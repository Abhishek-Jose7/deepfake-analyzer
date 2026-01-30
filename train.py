"""
Training script for DeepTrust Deepfake Detection Model
"""
import os
import argparse
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR

# Import model and dataset
from model.detector import DeepfakeDetector, create_model, LABELS
from model.dataset import create_dataloaders

# Metrics
try:
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ sklearn not available, limited metrics")


class Trainer:
    """
    Trainer class for deepfake detection model
    """
    
    def __init__(
        self,
        model: nn.Module,
        train_loader,
        val_loader,
        device: str = "cuda",
        learning_rate: float = 1e-4,
        weight_decay: float = 1e-5,
        epochs: int = 50,
        save_dir: str = "checkpoints",
        use_amp: bool = True,
        patience: int = 10
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.epochs = epochs
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.use_amp = use_amp and device == "cuda"
        self.patience = patience
        
        # Loss function with class weights for imbalance
        self.criterion = nn.CrossEntropyLoss()
        
        # Optimizer
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = OneCycleLR(
            self.optimizer,
            max_lr=learning_rate,  # FIXED: Removed * 10 multiplier to prevent divergence
            epochs=epochs,
            steps_per_epoch=len(train_loader)
        )
        
        # Mixed precision scaler
        self.scaler = GradScaler() if self.use_amp else None
        
        # Training history
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "val_auc": [],
            "learning_rate": []
        }
        
        self.best_val_acc = 0.0
        self.best_val_auc = 0.0
        self.epochs_without_improvement = 0
    
    def train_epoch(self) -> Tuple[float, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (frames, labels) in enumerate(self.train_loader):
            frames = frames.to(self.device)
            labels = labels.to(self.device)
            
            self.optimizer.zero_grad()
            
            if self.use_amp:
                with torch.amp.autocast('cuda'):
                    outputs = self.model(frames)
                    loss = self.criterion(outputs, labels)
                
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(frames)
                loss = self.criterion(outputs, labels)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()
            
            self.scheduler.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Progress update
            if (batch_idx + 1) % 10 == 0:
                print(f"  Batch {batch_idx + 1}/{len(self.train_loader)} | "
                      f"Loss: {loss.item():.4f} | "
                      f"Acc: {100. * correct / total:.2f}%", end='\r')
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = 100. * correct / total
        
        return avg_loss, accuracy
    
    @torch.no_grad()
    def validate(self) -> Dict[str, float]:
        """Validate the model"""
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_labels = []
        all_probs = []
        
        for frames, labels in self.val_loader:
            frames = frames.to(self.device)
            labels = labels.to(self.device)
            
            if self.use_amp:
                with torch.amp.autocast('cuda'):
                    outputs = self.model(frames)
                    loss = self.criterion(outputs, labels)
            else:
                outputs = self.model(frames)
                loss = self.criterion(outputs, labels)
            
            total_loss += loss.item()
            probs = torch.softmax(outputs, dim=1)
            _, predicted = outputs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs[:, 1].cpu().numpy())  # Probability of FAKE
        
        avg_loss = total_loss / len(self.val_loader)
        
        metrics = {"loss": avg_loss}
        
        if SKLEARN_AVAILABLE:
            metrics["accuracy"] = accuracy_score(all_labels, all_preds) * 100
            metrics["precision"] = precision_score(all_labels, all_preds, zero_division=0)
            metrics["recall"] = recall_score(all_labels, all_preds, zero_division=0)
            metrics["f1"] = f1_score(all_labels, all_preds, zero_division=0)
            try:
                metrics["auc"] = roc_auc_score(all_labels, all_probs)
            except:
                metrics["auc"] = 0.5
            
            cm = confusion_matrix(all_labels, all_preds)
            metrics["confusion_matrix"] = cm.tolist()
        else:
            correct = sum(p == l for p, l in zip(all_preds, all_labels))
            metrics["accuracy"] = 100. * correct / len(all_labels)
            metrics["auc"] = 0.5
        
        return metrics
    
    def save_checkpoint(self, epoch: int, metrics: Dict, is_best: bool = False):
        """Save model checkpoint"""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "metrics": metrics,
            "history": self.history
        }
        
        # Save latest
        torch.save(checkpoint, self.save_dir / "latest.pth")
        
        # Save best
        if is_best:
            torch.save(checkpoint, self.save_dir / "best.pth")
            print(f"  ✅ New best model saved!")
        
        # Save periodic checkpoints
        if epoch % 10 == 0:
            torch.save(checkpoint, self.save_dir / f"epoch_{epoch}.pth")
    
    def train(self) -> Dict:
        """Full training loop"""
        print("=" * 60)
        print("Starting Training")
        print(f"Device: {self.device}")
        print(f"Epochs: {self.epochs}")
        print(f"AMP: {self.use_amp}")
        print("=" * 60)
        
        start_time = time.time()
        
        for epoch in range(1, self.epochs + 1):
            print(f"\nEpoch {epoch}/{self.epochs}")
            print("-" * 40)
            
            # Train
            train_loss, train_acc = self.train_epoch()
            print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
            
            # Validate
            val_metrics = self.validate()
            val_acc = val_metrics["accuracy"]
            val_auc = val_metrics.get("auc", 0.5)
            print(f"  Val Loss: {val_metrics['loss']:.4f} | Val Acc: {val_acc:.2f}% | Val AUC: {val_auc:.4f}")
            
            # Update history
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_metrics["loss"])
            self.history["val_acc"].append(val_acc)
            self.history["val_auc"].append(val_auc)
            self.history["learning_rate"].append(self.optimizer.param_groups[0]["lr"])
            
            # Check for improvement
            is_best = val_acc > self.best_val_acc
            if is_best:
                self.best_val_acc = val_acc
                self.best_val_auc = val_auc
                self.epochs_without_improvement = 0
            else:
                self.epochs_without_improvement += 1
            
            # Save checkpoint
            self.save_checkpoint(epoch, val_metrics, is_best)
            
            # Early stopping
            if self.epochs_without_improvement >= self.patience:
                print(f"\n⚠️ Early stopping after {self.patience} epochs without improvement")
                break
        
        total_time = time.time() - start_time
        print("\n" + "=" * 60)
        print("Training Complete!")
        print(f"Total Time: {total_time / 60:.2f} minutes")
        print(f"Best Val Accuracy: {self.best_val_acc:.2f}%")
        print(f"Best Val AUC: {self.best_val_auc:.4f}")
        print("=" * 60)
        
        # Save final history
        with open(self.save_dir / "history.json", "w") as f:
            json.dump(self.history, f, indent=2)
        
        return self.history


def main():
    parser = argparse.ArgumentParser(description="Train DeepTrust Deepfake Detector")
    
    # Data arguments
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset")
    parser.add_argument("--dataset-type", type=str, default="generic",
                       choices=["generic", "faceforensics"], help="Dataset type")
    
    # Model arguments
    parser.add_argument("--backbone", type=str, default="efficientnet_b0",
                       help="Model backbone")
    parser.add_argument("--pretrained", action="store_true", default=True,
                       help="Use pretrained weights")
    parser.add_argument("--resume", type=str, default=None,
                       help="Path to checkpoint to resume from")
    
    # Training arguments
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=1e-5, help="Weight decay")
    parser.add_argument("--frames-per-video", type=int, default=16,
                       help="Frames to sample per video")
    parser.add_argument("--frame-size", type=int, default=224, help="Frame size")
    
    # Other arguments
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--workers", type=int, default=4, help="Data loading workers")
    parser.add_argument("--save-dir", type=str, default="checkpoints", help="Save directory")
    parser.add_argument("--patience", type=int, default=10, help="Early stopping patience")
    parser.add_argument("--no-amp", action="store_true", help="Disable mixed precision")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("DeepTrust Deepfake Detector Training")
    print("=" * 60)
    print(f"Dataset: {args.dataset}")
    print(f"Backbone: {args.backbone}")
    print(f"Device: {args.device}")
    print(f"Batch Size: {args.batch_size}")
    print(f"Epochs: {args.epochs}")
    print(f"Learning Rate: {args.lr}")
    print("=" * 60)
    
    # Create dataloaders
    train_loader, val_loader, test_loader = create_dataloaders(
        dataset_path=args.dataset,
        batch_size=args.batch_size,
        num_workers=args.workers,
        frames_per_video=args.frames_per_video,
        frame_size=(args.frame_size, args.frame_size),
        dataset_type=args.dataset_type
    )
    
    # Create model
    model = create_model(
        backbone=args.backbone,
        pretrained=args.pretrained,
        checkpoint_path=args.resume
    )
    
    print(f"\nModel Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Create trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=args.device,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        epochs=args.epochs,
        save_dir=args.save_dir,
        use_amp=not args.no_amp,
        patience=args.patience
    )
    
    # Train
    history = trainer.train()
    
    # Evaluate on test set if available
    if test_loader is not None:
        print("\nEvaluating on test set...")
        trainer.val_loader = test_loader
        test_metrics = trainer.validate()
        print(f"Test Accuracy: {test_metrics['accuracy']:.2f}%")
        print(f"Test AUC: {test_metrics.get('auc', 'N/A')}")
        
        with open(Path(args.save_dir) / "test_results.json", "w") as f:
            json.dump(test_metrics, f, indent=2)


if __name__ == "__main__":
    main()
