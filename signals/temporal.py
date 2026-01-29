"""
Temporal signal detection - the secret weapon
Deepfakes often fail over time, not per frame
"""
import cv2
import numpy as np


def temporal_consistency(frames):
    """
    Measure frame-to-frame consistency
    
    Deepfakes often have temporal instabilities that are invisible 
    in individual frames but visible across time.
    
    Args:
        frames: List of frames in sequence
        
    Returns:
        Score between 0 and 1 (higher = more consistent/trustworthy)
    """
    if len(frames) < 2:
        return 0.5  # Ambiguous with single frame
    
    diffs = []
    for i in range(len(frames) - 1):
        diff = cv2.absdiff(frames[i], frames[i + 1])
        diffs.append(diff.mean())
    
    avg_diff = sum(diffs) / len(diffs)
    
    # Low consistency = high difference = suspicious
    # Typical videos have mean diff of 5-15
    # Deepfakes often have higher temporal instability
    score = 1.0 - min(1.0, avg_diff / 20)
    
    return score


def temporal_variance(frames):
    """
    Measure variance in temporal changes
    
    Real videos have relatively stable temporal patterns.
    Deepfakes often have erratic temporal changes.
    
    Args:
        frames: List of frames in sequence
        
    Returns:
        Score between 0 and 1 (higher = more stable)
    """
    if len(frames) < 3:
        return 0.5
    
    diffs = []
    for i in range(len(frames) - 1):
        diff = cv2.absdiff(frames[i], frames[i + 1])
        diffs.append(diff.mean())
    
    # Calculate variance of differences
    variance = np.var(diffs)
    
    # Lower variance = more stable = more trustworthy
    # Typical variance is 1-10
    score = 1.0 - min(1.0, variance / 10)
    
    return score


def optical_flow_consistency(frames):
    """
    Analyze optical flow between frames
    
    Deepfakes may have inconsistent motion patterns
    
    Args:
        frames: List of frames in sequence
        
    Returns:
        Score between 0 and 1 (higher = more consistent motion)
    """
    if len(frames) < 2:
        return 0.5
    
    flow_magnitudes = []
    
    for i in range(min(10, len(frames) - 1)):  # Sample first 10 frame pairs
        prev_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        next_gray = cv2.cvtColor(frames[i + 1], cv2.COLOR_BGR2GRAY)
        
        # Calculate dense optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, next_gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        # Calculate flow magnitude
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        flow_magnitudes.append(np.mean(magnitude))
    
    # Check consistency of flow magnitudes
    if len(flow_magnitudes) < 2:
        return 0.5
    
    variance = np.var(flow_magnitudes)
    
    # Lower variance = more consistent = more trustworthy
    score = 1.0 - min(1.0, variance / 5)
    
    return score


def analyze_temporal_signals(frames):
    """
    Comprehensive temporal analysis
    
    Args:
        frames: List of frames in sequence
        
    Returns:
        Dictionary with temporal scores and combined score
    """
    consistency = temporal_consistency(frames)
    variance = temporal_variance(frames)
    optical_flow = optical_flow_consistency(frames)
    
    # Weighted combination
    combined = 0.5 * consistency + 0.3 * variance + 0.2 * optical_flow
    
    return {
        'consistency': consistency,
        'variance': variance,
        'optical_flow': optical_flow,
        'combined': combined
    }
