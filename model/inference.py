"""
Inference module for DeepTrust Deepfake Detection
Integrates trained model with the API
"""
import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import torch

# Try imports
try:
    from torchvision import transforms
    TORCHVISION_AVAILABLE = True
except ImportError:
    TORCHVISION_AVAILABLE = False

from model.detector import create_model, DeepfakeDetector, LABELS


class DeepfakeInference:
    """
    Inference engine for deepfake detection
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        backbone: str = "efficientnet_b0",
        device: Optional[str] = None,
        frame_size: Tuple[int, int] = (224, 224),
        num_frames: int = 16
    ):
        """
        Initialize inference engine
        
        Args:
            model_path: Path to trained model checkpoint
            backbone: Model backbone architecture
            device: Device to run on (cuda/cpu)
            frame_size: Input frame size
            num_frames: Number of frames to sample from video
        """
        # Set device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        self.frame_size = frame_size
        self.num_frames = num_frames
        self.model_loaded = False
        
        # Initialize face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Try to load model
        self._load_model(model_path, backbone)
        
        # Setup transforms
        if TORCHVISION_AVAILABLE:
            self.transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(frame_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                   std=[0.229, 0.224, 0.225])
            ])
        else:
            self.transform = None
    
    def _load_model(self, model_path: Optional[str], backbone: str):
        """Load the detection model"""
        # Check for model in standard locations
        possible_paths = [
            model_path,
            "checkpoints/best.pth",
            "checkpoints/latest.pth",
            "model/pretrained/best.pth",
            os.environ.get("DEEPTRUST_MODEL_PATH")
        ]
        
        checkpoint_path = None
        for path in possible_paths:
            if path and os.path.exists(path):
                checkpoint_path = path
                break
        
        try:
            self.model = create_model(
                backbone=backbone,
                pretrained=True,
                checkpoint_path=checkpoint_path
            )
            self.model.to(self.device)
            self.model.eval()
            
            if checkpoint_path:
                print(f"✅ Model loaded from {checkpoint_path}")
                self.model_loaded = True
            else:
                print("⚠️ No trained checkpoint found, using pretrained backbone only")
                self.model_loaded = False
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.model_loaded = False
    
    def _crop_face(self, frame: np.ndarray) -> np.ndarray:
        """Extract face region from frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get largest face
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            
            # Add margin
            margin = int(0.2 * max(w, h))
            x_start = max(0, x - margin)
            y_start = max(0, y - margin)
            x_end = min(frame.shape[1], x + w + margin)
            y_end = min(frame.shape[0], y + h + margin)
            
            return frame[y_start:y_end, x_start:x_end]
        
        return frame
    
    def _preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess a single frame"""
        # Ensure RGB
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        elif frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Crop face
        face = self._crop_face(frame)
        
        # Resize
        face = cv2.resize(face, self.frame_size)
        
        # Apply transform
        if self.transform:
            tensor = self.transform(face)
        else:
            tensor = torch.from_numpy(face).permute(2, 0, 1).float() / 255.0
        
        return tensor
    
    def _extract_frames(self, video_path: str) -> List[np.ndarray]:
        """Extract frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            return frames
        
        # Sample frames evenly
        indices = np.linspace(0, total_frames - 1, self.num_frames, dtype=int)
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        
        cap.release()
        return frames
    
    @torch.no_grad()
    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze a video for deepfake detection
        
        Args:
            video_path: Path to video file
            
        Returns:
            Analysis results dictionary
        """
        if self.model is None:
            return {
                "success": False,
                "error": "Model not loaded",
                "prediction": "unknown",
                "confidence": 0.0,
                "probabilities": {"real": 0.5, "fake": 0.5}
            }
        
        # Extract frames
        frames = self._extract_frames(video_path)
        
        if len(frames) == 0:
            return {
                "success": False,
                "error": "Could not extract frames from video",
                "prediction": "unknown",
                "confidence": 0.0,
                "probabilities": {"real": 0.5, "fake": 0.5}
            }
        
        # Preprocess frames
        processed_frames = []
        for frame in frames:
            try:
                tensor = self._preprocess_frame(frame)
                processed_frames.append(tensor)
            except Exception as e:
                continue
        
        if len(processed_frames) == 0:
            return {
                "success": False,
                "error": "Frame preprocessing failed",
                "prediction": "unknown",
                "confidence": 0.0,
                "probabilities": {"real": 0.5, "fake": 0.5}
            }
        
        # Pad if needed
        while len(processed_frames) < self.num_frames:
            processed_frames.append(processed_frames[-1])
        
        # Stack frames: (1, T, C, H, W)
        frames_tensor = torch.stack(processed_frames[:self.num_frames]).unsqueeze(0)
        frames_tensor = frames_tensor.to(self.device)
        
        # Run inference
        self.model.eval()
        outputs = self.model(frames_tensor)
        probs = torch.softmax(outputs, dim=1)
        
        # Get prediction
        confidence, prediction = probs.max(dim=1)
        prediction = prediction.item()
        confidence = confidence.item()
        
        # Get class probabilities
        real_prob = probs[0, 0].item()
        fake_prob = probs[0, 1].item()
        
        return {
            "success": True,
            "prediction": LABELS[prediction],
            "is_fake": prediction == 1,
            "confidence": confidence,
            "probabilities": {
                "real": real_prob,
                "fake": fake_prob
            },
            "frames_analyzed": len(processed_frames),
            "model_loaded": self.model_loaded
        }
    
    @torch.no_grad()
    def analyze_frames(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """
        Analyze pre-extracted frames
        
        Args:
            frames: List of video frames (numpy arrays)
            
        Returns:
            Analysis results dictionary
        """
        if self.model is None:
            return {
                "success": False,
                "error": "Model not loaded",
                "prediction": "unknown",
                "confidence": 0.0,
                "score": 0.5
            }
        
        if len(frames) == 0:
            return {
                "success": False,
                "error": "No frames provided",
                "prediction": "unknown",
                "confidence": 0.0,
                "score": 0.5
            }
        
        # Preprocess frames
        processed_frames = []
        for frame in frames:
            try:
                tensor = self._preprocess_frame(frame)
                processed_frames.append(tensor)
            except:
                continue
        
        if len(processed_frames) == 0:
            return {
                "success": False,
                "error": "Frame preprocessing failed",
                "prediction": "unknown",
                "confidence": 0.0,
                "score": 0.5
            }
        
        # Sample frames if too many
        if len(processed_frames) > self.num_frames:
            indices = np.linspace(0, len(processed_frames) - 1, self.num_frames, dtype=int)
            processed_frames = [processed_frames[i] for i in indices]
        
        # Pad if needed
        while len(processed_frames) < self.num_frames:
            processed_frames.append(processed_frames[-1])
        
        # Stack frames
        frames_tensor = torch.stack(processed_frames[:self.num_frames]).unsqueeze(0)
        frames_tensor = frames_tensor.to(self.device)
        
        # Run inference
        self.model.eval()
        outputs = self.model(frames_tensor)
        probs = torch.softmax(outputs, dim=1)
        
        confidence, prediction = probs.max(dim=1)
        prediction = prediction.item()
        confidence = confidence.item()
        
        real_prob = probs[0, 0].item()
        fake_prob = probs[0, 1].item()
        
        # Return score (higher = more authentic)
        return {
            "success": True,
            "prediction": LABELS[prediction],
            "is_fake": prediction == 1,
            "confidence": confidence,
            "score": real_prob,  # Trust score (probability of being real)
            "probabilities": {
                "real": real_prob,
                "fake": fake_prob
            },
            "frames_analyzed": len(processed_frames),
            "model_loaded": self.model_loaded
        }


# Global inference instance
_inference_engine: Optional[DeepfakeInference] = None


def get_inference_engine() -> DeepfakeInference:
    """Get or create the inference engine singleton"""
    global _inference_engine
    if _inference_engine is None:
        _inference_engine = DeepfakeInference()
    return _inference_engine


def analyze_video(video_path: str) -> Dict[str, Any]:
    """
    Main entry point for video analysis
    
    Args:
        video_path: Path to video file
        
    Returns:
        Analysis results
    """
    engine = get_inference_engine()
    return engine.analyze_video(video_path)


def analyze_frames(frames: List[np.ndarray]) -> Dict[str, Any]:
    """
    Analyze frames directly
    
    Args:
        frames: List of video frames
        
    Returns:
        Analysis results
    """
    engine = get_inference_engine()
    return engine.analyze_frames(frames)
