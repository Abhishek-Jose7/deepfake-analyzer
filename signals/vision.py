"""
Vision-based signal detection for deepfake artifacts
Uses classical computer vision techniques to detect unnatural textures
"""
import cv2
import numpy as np


def artifact_score(frame):
    """
    Detect visual artifacts using Laplacian variance
    
    Lower variance indicates over-smoothing, which is suspicious.
    This is a classic forensic technique.
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Score between 0 and 1 (higher = more trustworthy)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    variance = lap.var()
    
    # Lower variance → over-smoothed → suspicious
    # Normalize: typical real videos have variance 500-2000
    score = min(1.0, variance / 1000)
    return score


def edge_consistency_score(frame):
    """
    Measure edge consistency - deepfakes often have inconsistent edges around faces
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Score between 0 and 1 (higher = more consistent edges)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(gray, 100, 200)
    
    # Calculate edge density
    edge_density = np.mean(edges) / 255.0
    
    # Good videos have moderate edge density (0.1 - 0.3)
    # Too low or too high is suspicious
    if 0.1 <= edge_density <= 0.3:
        score = 1.0
    elif edge_density < 0.1:
        score = edge_density / 0.1
    else:
        score = max(0.0, 1.0 - (edge_density - 0.3) / 0.3)
    
    return score


def analyze_frame(frame):
    """
    Comprehensive vision analysis of a single frame
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Dictionary with vision scores
    """
    artifact = artifact_score(frame)
    edge_consistency = edge_consistency_score(frame)
    
    # Combined vision score (weighted average)
    combined = 0.6 * artifact + 0.4 * edge_consistency
    
    return {
        'artifact_score': artifact,
        'edge_consistency': edge_consistency,
        'combined': combined
    }


def analyze_frames(frames):
    """
    Analyze multiple frames and aggregate results
    
    Args:
        frames: List of frames
        
    Returns:
        Aggregated vision signal score
    """
    if not frames:
        return 0.0
    
    scores = [analyze_frame(frame)['combined'] for frame in frames]
    return np.mean(scores)
