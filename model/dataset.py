"""
Dataset classes for deepfake detection training
Supports FaceForensics++, Celeb-DF, DFDC, and custom datasets
"""
import os
import cv2
import json
import random
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List, Callable, Dict
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler

try:
    from torchvision import transforms
    TORCHVISION_AVAILABLE = True
except ImportError:
    TORCHVISION_AVAILABLE = False


class VideoFrameDataset(Dataset):
    """
    Dataset for loading video frames for deepfake detection
    
    Expected directory structure:
    dataset/
    ├── real/
    │   ├── video1/
    │   │   ├── frame_001.jpg
    │   │   ├── frame_002.jpg
    │   │   └── ...
    │   └── video2/
    └── fake/
        ├── video1/
        └── video2/
    
    OR with video files:
    dataset/
    ├── real/
    │   ├── video1.mp4
    │   └── video2.mp4
    └── fake/
        ├── video1.mp4
        └── video2.mp4
    """
    
    def __init__(
        self,
        root_dir: str,
        split: str = "train",
        transform: Optional[Callable] = None,
        frames_per_video: int = 16,
        frame_size: Tuple[int, int] = (224, 224),
        use_face_crop: bool = True
    ):
        self.root_dir = Path(root_dir)
        self.split = split
        self.transform = transform
        self.frames_per_video = frames_per_video
        self.frame_size = frame_size
        self.use_face_crop = use_face_crop
        
        # Load face detector if needed
        if use_face_crop:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        
        # Build sample list
        self.samples = []
        self._build_dataset()
        
        # Default transform
        if self.transform is None and TORCHVISION_AVAILABLE:
            if split == "train":
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.RandomHorizontalFlip(0.5),
                    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
                    transforms.RandomRotation(10),
                    transforms.Resize(frame_size),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                       std=[0.229, 0.224, 0.225])
                ])
            else:
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.Resize(frame_size),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                       std=[0.229, 0.224, 0.225])
                ])
    
    def _build_dataset(self):
        """Build list of samples from directory"""
        real_dir = self.root_dir / self.split / "real"
        fake_dir = self.root_dir / self.split / "fake"
        
        # Also try without split subdirectory
        if not real_dir.exists():
            real_dir = self.root_dir / "real"
            fake_dir = self.root_dir / "fake"
        
        if real_dir.exists():
            for item in real_dir.iterdir():
                if item.is_dir():
                    # Directory with frames
                    self.samples.append({"path": str(item), "label": 0, "type": "frames"})
                elif item.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                    # Video file
                    self.samples.append({"path": str(item), "label": 0, "type": "video"})
        
        if fake_dir.exists():
            for item in fake_dir.iterdir():
                if item.is_dir():
                    self.samples.append({"path": str(item), "label": 1, "type": "frames"})
                elif item.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                    self.samples.append({"path": str(item), "label": 1, "type": "video"})
        
        print(f"Loaded {len(self.samples)} samples for {self.split} split")
        print(f"  Real: {sum(1 for s in self.samples if s['label'] == 0)}")
        print(f"  Fake: {sum(1 for s in self.samples if s['label'] == 1)}")
    
    def _extract_frames_from_video(self, video_path: str) -> List[np.ndarray]:
        """Extract frames from video file"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            return frames
        
        # Sample frames evenly
        indices = np.linspace(0, total_frames - 1, self.frames_per_video, dtype=int)
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
        
        cap.release()
        return frames
    
    def _load_frames_from_dir(self, dir_path: str) -> List[np.ndarray]:
        """Load frames from directory"""
        dir_path = Path(dir_path)
        frame_files = sorted([
            f for f in dir_path.iterdir()
            if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']
        ])
        
        if len(frame_files) == 0:
            return []
        
        # Sample frames evenly
        indices = np.linspace(0, len(frame_files) - 1, self.frames_per_video, dtype=int)
        
        frames = []
        for idx in indices:
            frame = cv2.imread(str(frame_files[idx]))
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
        
        return frames
    
    def _crop_face(self, frame: np.ndarray) -> np.ndarray:
        """Crop face region from frame"""
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
            
            face = frame[y_start:y_end, x_start:x_end]
            return cv2.resize(face, self.frame_size)
        
        # No face found, resize whole frame
        return cv2.resize(frame, self.frame_size)
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        sample = self.samples[idx]
        
        # Load frames
        if sample["type"] == "video":
            frames = self._extract_frames_from_video(sample["path"])
        else:
            frames = self._load_frames_from_dir(sample["path"])
        
        if len(frames) == 0:
            # Return dummy data if loading fails
            dummy = torch.zeros(self.frames_per_video, 3, *self.frame_size)
            return dummy, sample["label"]
        
        # Process frames
        processed_frames = []
        for frame in frames:
            if self.use_face_crop:
                frame = self._crop_face(frame)
            else:
                frame = cv2.resize(frame, self.frame_size)
            
            if self.transform:
                frame = self.transform(frame)
            else:
                frame = torch.from_numpy(frame).permute(2, 0, 1).float() / 255.0
            
            processed_frames.append(frame)
        
        # Pad if not enough frames
        while len(processed_frames) < self.frames_per_video:
            processed_frames.append(processed_frames[-1])
        
        # Stack frames: (T, C, H, W)
        frames_tensor = torch.stack(processed_frames[:self.frames_per_video])
        
        return frames_tensor, sample["label"]


class FaceForensicsDataset(VideoFrameDataset):
    """
    Dataset loader for FaceForensics++ dataset
    
    Expected structure:
    faceforensics/
    ├── original_sequences/
    │   └── youtube/
    │       └── c23/
    │           └── videos/
    └── manipulated_sequences/
        ├── Deepfakes/
        ├── Face2Face/
        ├── FaceSwap/
        └── NeuralTextures/
    """
    
    def __init__(
        self,
        root_dir: str,
        compression: str = "c23",  # c23, c40, raw
        manipulation: str = "all",  # Deepfakes, Face2Face, FaceSwap, NeuralTextures, all
        split: str = "train",
        split_file: Optional[str] = None,
        **kwargs
    ):
        self.compression = compression
        self.manipulation = manipulation
        self.split_file = split_file
        
        # Don't call parent init yet
        self.root_dir = Path(root_dir)
        self.split = split
        self.frames_per_video = kwargs.get('frames_per_video', 16)
        self.frame_size = kwargs.get('frame_size', (224, 224))
        self.use_face_crop = kwargs.get('use_face_crop', True)
        self.transform = kwargs.get('transform', None)
        
        if self.use_face_crop:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        
        self.samples = []
        self._build_ff_dataset()
        
        # Setup transforms
        if self.transform is None and TORCHVISION_AVAILABLE:
            if split == "train":
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.RandomHorizontalFlip(0.5),
                    transforms.ColorJitter(brightness=0.2, contrast=0.2),
                    transforms.Resize(self.frame_size),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                       std=[0.229, 0.224, 0.225])
                ])
            else:
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.Resize(self.frame_size),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                       std=[0.229, 0.224, 0.225])
                ])
    
    def _build_ff_dataset(self):
        """Build FaceForensics++ dataset"""
        # Real videos
        real_dir = self.root_dir / "original_sequences" / "youtube" / self.compression / "videos"
        if real_dir.exists():
            for video in real_dir.glob("*.mp4"):
                self.samples.append({"path": str(video), "label": 0, "type": "video"})
        
        # Fake videos
        manipulations = ["Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures"]
        if self.manipulation != "all":
            manipulations = [self.manipulation]
        
        for manip in manipulations:
            fake_dir = self.root_dir / "manipulated_sequences" / manip / self.compression / "videos"
            if fake_dir.exists():
                for video in fake_dir.glob("*.mp4"):
                    self.samples.append({"path": str(video), "label": 1, "type": "video"})
        
        # Apply train/val/test split if split file provided
        if self.split_file and os.path.exists(self.split_file):
            with open(self.split_file, 'r') as f:
                splits = json.load(f)
            if self.split in splits:
                split_ids = set(splits[self.split])
                self.samples = [
                    s for s in self.samples
                    if Path(s["path"]).stem.split("_")[0] in split_ids
                ]
        
        print(f"FaceForensics++ {self.split}: {len(self.samples)} samples")


def create_dataloaders(
    dataset_path: str,
    batch_size: int = 16,
    num_workers: int = 4,
    frames_per_video: int = 16,
    frame_size: Tuple[int, int] = (224, 224),
    dataset_type: str = "generic"  # generic, faceforensics
) -> Tuple[DataLoader, DataLoader, Optional[DataLoader]]:
    """
    Create train, validation, and test dataloaders
    
    Args:
        dataset_path: Path to dataset
        batch_size: Batch size
        num_workers: Number of data loading workers
        frames_per_video: Frames to sample per video
        frame_size: Frame resize dimensions
        dataset_type: Type of dataset structure
        
    Returns:
        train_loader, val_loader, test_loader (optional)
    """
    DatasetClass = FaceForensicsDataset if dataset_type == "faceforensics" else VideoFrameDataset
    
    train_dataset = DatasetClass(
        root_dir=dataset_path,
        split="train",
        frames_per_video=frames_per_video,
        frame_size=frame_size
    )
    
    val_dataset = DatasetClass(
        root_dir=dataset_path,
        split="val",
        frames_per_video=frames_per_video,
        frame_size=frame_size
    )
    
    # Weighted sampler for imbalanced data
    labels = [s["label"] for s in train_dataset.samples]
    class_counts = [labels.count(0), labels.count(1)]
    weights = [1.0 / class_counts[l] for l in labels]
    sampler = WeightedRandomSampler(weights, len(weights))
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    # Test loader (optional)
    test_loader = None
    test_dir = Path(dataset_path) / "test"
    if test_dir.exists():
        test_dataset = DatasetClass(
            root_dir=dataset_path,
            split="test",
            frames_per_video=frames_per_video,
            frame_size=frame_size
        )
        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True
        )
    
    return train_loader, val_loader, test_loader
