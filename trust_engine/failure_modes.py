"""
Failure mode detection - CRITICAL for trust calibration
Detects input quality degradation
"""
import cv2
import numpy as np


def compression_level(frame):
    """
    Detect compression artifacts
    
    Heavy compression makes deepfake detection harder.
    We need to reduce confidence when input quality is poor.
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Score between 0 and 1 (higher = less compression)
    """
    edges = cv2.Canny(frame, 100, 200)
    edge_density = edges.mean() / 255.0
    
    # Low edge density suggests heavy compression
    # Typical uncompressed videos: 0.15-0.3
    # Heavily compressed: < 0.1
    
    if edge_density >= 0.15:
        score = 1.0
    else:
        score = edge_density / 0.15
    
    return score


def blocking_artifacts(frame):
    """
    Detect blocking artifacts from compression
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Score between 0 and 1 (higher = fewer blocks)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply DCT to detect 8x8 block boundaries
    # This is simplified - real implementation would analyze block boundaries
    
    # For now, use gradient analysis
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    
    # High gradient variance suggests blocking
    variance = np.var(gradient_magnitude)
    
    # Normalize
    score = 1.0 - min(1.0, variance / 10000)
    
    return score


def noise_level(frame):
    """
    Estimate noise level in frame
    
    High noise makes analysis unreliable
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Score between 0 and 1 (higher = less noise)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use median filtering to estimate noise
    blurred = cv2.medianBlur(gray, 5)
    noise = cv2.absdiff(gray, blurred)
    
    noise_level = np.mean(noise)
    
    # Typical noise: 2-10
    # High noise: > 15
    
    if noise_level <= 10:
        score = 1.0
    else:
        score = max(0.0, 1.0 - (noise_level - 10) / 20)
    
    return score


def resolution_quality(frame):
    """
    Check if resolution is sufficient for analysis
    
    Args:
        frame: Input frame
        
    Returns:
        Score between 0 and 1 (higher = better resolution)
    """
    height, width = frame.shape[:2]
    
    # Minimum recommended: 480p (640x480)
    # Good: 720p (1280x720)
    
    pixels = height * width
    
    if pixels >= 1280 * 720:
        score = 1.0
    elif pixels >= 640 * 480:
        score = 0.7
    else:
        score = max(0.3, pixels / (640 * 480))
    
    return score


def analyze_quality(frames):
    """
    Comprehensive quality analysis
    
    This is critical - it tells us how confident we can be in our analysis
    
    Args:
        frames: List of frames
        
    Returns:
        Dictionary with quality scores
    """
    if not frames:
        return {
            'compression': 0.0,
            'blocking': 0.0,
            'noise': 0.0,
            'resolution': 0.0,
            'overall': 0.0
        }
    
    # Sample a few frames
    sample_frames = frames[::max(1, len(frames) // 5)][:5]
    
    compression_scores = [compression_level(f) for f in sample_frames]
    blocking_scores = [blocking_artifacts(f) for f in sample_frames]
    noise_scores = [noise_level(f) for f in sample_frames]
    resolution_scores = [resolution_quality(f) for f in sample_frames]
    
    compression = np.mean(compression_scores)
    blocking = np.mean(blocking_scores)
    noise = np.mean(noise_scores)
    resolution = np.mean(resolution_scores)
    
    # Overall quality (all factors matter)
    overall = 0.3 * compression + 0.2 * blocking + 0.2 * noise + 0.3 * resolution
    
    return {
        'compression': compression,
        'blocking': blocking,
        'noise': noise,
        'resolution': resolution,
        'overall': overall
    }
