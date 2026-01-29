"""
Video utilities for frame extraction and processing
"""
import cv2
import numpy as np


def extract_frames(video_path, fps=5):
    """
    Extract frames from video at specified FPS
    
    Args:
        video_path: Path to video file
        fps: Extract every Nth frame (default: 5)
        
    Returns:
        List of frames as numpy arrays
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / fps) if original_fps > fps else 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1

    cap.release()
    return frames


def get_video_metadata(video_path):
    """
    Extract metadata from video file
    
    Returns:
        Dictionary with video metadata
    """
    cap = cv2.VideoCapture(video_path)
    
    metadata = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0
    }
    
    cap.release()
    return metadata
