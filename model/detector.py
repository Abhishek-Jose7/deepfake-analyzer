"""
DeepTrust Deepfake Detection Model
EfficientNet-based binary classifier for deepfake detection
"""
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List
import numpy as np

# Try to import timm for EfficientNet, fallback to torchvision
try:
    import timm
    TIMM_AVAILABLE = True
except ImportError:
    TIMM_AVAILABLE = False
    print("⚠️ timm not available, using basic model")


class AttentionBlock(nn.Module):
    """
    Self-attention block for focusing on manipulated regions
    """
    def __init__(self, in_channels: int):
        super().__init__()
        self.query = nn.Conv2d(in_channels, in_channels // 8, 1)
        self.key = nn.Conv2d(in_channels, in_channels // 8, 1)
        self.value = nn.Conv2d(in_channels, in_channels, 1)
        self.gamma = nn.Parameter(torch.zeros(1))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, C, H, W = x.size()
        
        # Query, Key, Value projections
        q = self.query(x).view(batch, -1, H * W).permute(0, 2, 1)
        k = self.key(x).view(batch, -1, H * W)
        v = self.value(x).view(batch, -1, H * W)
        
        # Attention weights
        attention = F.softmax(torch.bmm(q, k), dim=-1)
        
        # Apply attention
        out = torch.bmm(v, attention.permute(0, 2, 1))
        out = out.view(batch, C, H, W)
        
        return self.gamma * out + x


class DeepfakeDetector(nn.Module):
    """
    Main deepfake detection model
    
    Architecture:
    - EfficientNet backbone (pretrained on ImageNet)
    - Attention mechanism for artifact focus
    - Multi-scale feature fusion
    - Binary classification head
    """
    
    def __init__(
        self,
        backbone: str = "efficientnet_b0",
        pretrained: bool = True,
        num_classes: int = 2,
        dropout: float = 0.3
    ):
        super().__init__()
        
        self.backbone_name = backbone
        
        if TIMM_AVAILABLE:
            # Use timm for EfficientNet
            self.backbone = timm.create_model(
                backbone,
                pretrained=pretrained,
                num_classes=0,  # Remove classifier
                global_pool=''  # Remove global pooling
            )
            
            # Get feature dimensions
            with torch.no_grad():
                dummy = torch.zeros(1, 3, 224, 224)
                features = self.backbone(dummy)
                self.feature_dim = features.shape[1]
        else:
            # Fallback to simpler CNN
            self.backbone = self._build_simple_backbone()
            self.feature_dim = 512
        
        # Attention module
        self.attention = AttentionBlock(self.feature_dim)
        
        # Global pooling
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(self.feature_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout / 2),
            nn.Linear(256, num_classes)
        )
        
        # For multi-frame analysis
        self.temporal_pool = nn.AdaptiveAvgPool1d(1)
    
    def _build_simple_backbone(self) -> nn.Module:
        """Fallback CNN backbone"""
        return nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Block 2
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Block 3
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Block 4
            nn.Conv2d(256, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # Block 5
            nn.Conv2d(512, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
        )
    
    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extract features from input image"""
        features = self.backbone(x)
        features = self.attention(features)
        features = self.global_pool(features)
        return features.flatten(1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            x: Input tensor of shape (B, C, H, W) or (B, T, C, H, W) for video
            
        Returns:
            Logits of shape (B, num_classes)
        """
        if x.dim() == 5:
            # Video input: (B, T, C, H, W)
            B, T, C, H, W = x.shape
            x = x.view(B * T, C, H, W)
            features = self.extract_features(x)
            features = features.view(B, T, -1)
            # Temporal pooling
            features = features.permute(0, 2, 1)
            features = self.temporal_pool(features).squeeze(-1)
        else:
            # Single image: (B, C, H, W)
            features = self.extract_features(x)
        
        return self.classifier(features)
    
    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        """Get probability scores"""
        logits = self.forward(x)
        return F.softmax(logits, dim=-1)
    
    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Make prediction
        
        Returns:
            (predictions, confidence scores)
        """
        probs = self.predict_proba(x)
        confidence, predictions = probs.max(dim=-1)
        return predictions, confidence


class DeepfakeDetectorEnsemble(nn.Module):
    """
    Ensemble of multiple models for robust detection
    """
    
    def __init__(self, models: List[DeepfakeDetector]):
        super().__init__()
        self.models = nn.ModuleList(models)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        outputs = [model(x) for model in self.models]
        return torch.stack(outputs).mean(dim=0)
    
    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        probs = [model.predict_proba(x) for model in self.models]
        return torch.stack(probs).mean(dim=0)


def create_model(
    backbone: str = "efficientnet_b0",
    pretrained: bool = True,
    checkpoint_path: Optional[str] = None
) -> DeepfakeDetector:
    """
    Create and optionally load a deepfake detection model
    
    Args:
        backbone: Model backbone (efficientnet_b0, efficientnet_b3, etc.)
        pretrained: Whether to use ImageNet pretrained weights
        checkpoint_path: Path to trained checkpoint
        
    Returns:
        DeepfakeDetector model
    """
    model = DeepfakeDetector(
        backbone=backbone,
        pretrained=pretrained,
        num_classes=2,
        dropout=0.3
    )
    
    if checkpoint_path and os.path.exists(checkpoint_path):
        print(f"Loading checkpoint from {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        print("✅ Checkpoint loaded successfully")
    
    return model


# Label mappings
LABELS = {0: "REAL", 1: "FAKE"}
LABEL_TO_IDX = {"REAL": 0, "FAKE": 1}
