"""
Video Processing Utilities for DeepTrust API
"""
import cv2
import numpy as np
import subprocess
import os
import tempfile


def extract_frames(video_path, max_frames=30, fps=5):
    """
    Extract frames from video file
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames to extract
        fps: Target frames per second
        
    Returns:
        List of numpy arrays (BGR format)
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    if not cap.isOpened():
        return frames
    
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(original_fps / fps)) if original_fps > fps else 1
    count = 0
    
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1
    
    cap.release()
    return frames


def extract_audio(video_path):
    """
    Extract audio from video and save as WAV
    
    Args:
        video_path: Path to video file
        
    Returns:
        Path to extracted audio file, or None if no audio
    """
    try:
        # Create temp file for audio
        audio_path = tempfile.mktemp(suffix=".wav")
        
        # Try using ffmpeg if available
        try:
            result = subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                audio_path
            ], capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(audio_path):
                return audio_path
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Fallback: try moviepy
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            if clip.audio is not None:
                clip.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec='pcm_s16le', verbose=False, logger=None)
                clip.close()
                return audio_path
            clip.close()
        except Exception:
            pass
        
        return None
        
    except Exception:
        return None


def get_video_metadata(video_path):
    """
    Get video metadata
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with video properties
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return {}
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    cap.release()
    
    return {
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration": duration,
        "resolution": f"{width}x{height}"
    }
