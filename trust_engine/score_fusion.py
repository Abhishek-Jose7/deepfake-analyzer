"""
Trust Score Fusion Module
Combines multiple signals into a final trust score
"""
import cv2
import numpy as np


def assess_quality(frames):
    """
    Assess the quality of input video frames
    
    Args:
        frames: List of video frames
        
    Returns:
        Dictionary with quality metrics
    """
    if not frames:
        return {"overall": 0.5}
    
    # Sample frame for analysis
    frame = frames[len(frames) // 2]
    
    # Resolution quality
    height, width = frame.shape[:2]
    resolution_score = min(1.0, (width * height) / (1280 * 720))
    
    # Compression quality (using Laplacian)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    compression_score = min(1.0, laplacian_var / 500)
    
    # Noise estimation
    noise = np.std(gray) / 255.0
    noise_score = 1.0 - min(1.0, noise * 3)
    
    # Blocking artifact detection
    h, w = gray.shape
    block_diff = 0
    for i in range(8, h, 8):
        block_diff += np.abs(float(gray[i-1, :].mean()) - float(gray[i, :].mean()))
    blocking_score = 1.0 - min(1.0, block_diff / (h / 8) / 10)
    
    # Overall quality
    overall = 0.3 * resolution_score + 0.3 * compression_score + 0.2 * noise_score + 0.2 * blocking_score
    
    return {
        "overall": overall,
        "resolution": resolution_score,
        "compression": compression_score,
        "noise": noise_score,
        "blocking": blocking_score
    }


def calculate_trust_score(signals):
    """
    Calculate final trust score from individual signals
    
    Args:
        signals: Dictionary containing vision, audio, temporal scores
        
    Returns:
        Tuple of (trust_score, quality_assessment)
    """
    vision_score = signals.get("vision", {}).get("score", 0.5)
    audio_score = signals.get("audio", {}).get("score", 0.5)
    temporal_score = signals.get("temporal", {}).get("score", 0.5)
    
    # Weighted combination
    # Vision is most reliable, temporal catches time-based issues
    weights = {"vision": 0.4, "audio": 0.3, "temporal": 0.3}
    
    trust_score = (
        vision_score * weights["vision"] +
        audio_score * weights["audio"] +
        temporal_score * weights["temporal"]
    )
    
    # Calculate confidence based on signal consistency
    scores = [vision_score, audio_score, temporal_score]
    consistency = 1.0 - np.std(scores)
    
    quality = {
        "overall": consistency,
        "signal_consistency": consistency
    }
    
    return trust_score, quality


def generate_report(trust_score, signals, quality_assessment):
    """
    Generate a human-readable report
    
    Args:
        trust_score: Final trust score
        signals: Individual signal scores
        quality_assessment: Quality metrics
        
    Returns:
        Dictionary with decision and explanation
    """
    # Determine decision
    if trust_score >= 0.7:
        decision = "Likely Real"
        confidence = "high"
    elif trust_score >= 0.55:
        decision = "Possibly Real"
        confidence = "medium"
    elif trust_score >= 0.45:
        decision = "Ambiguous"
        confidence = "low"
    elif trust_score >= 0.3:
        decision = "Possibly Fake"
        confidence = "medium"
    else:
        decision = "Likely Fake"
        confidence = "high"
    
    # Generate reason
    reasons = []
    
    vision_score = signals.get("vision", {}).get("score", 0.5)
    audio_score = signals.get("audio", {}).get("score", 0.5)
    temporal_score = signals.get("temporal", {}).get("score", 0.5)
    
    if vision_score < 0.4:
        reasons.append("visual artifacts detected")
    elif vision_score > 0.7:
        reasons.append("clean visual quality")
    
    if audio_score < 0.4:
        reasons.append("synthetic audio patterns")
    elif audio_score > 0.7:
        reasons.append("natural audio characteristics")
    
    if temporal_score < 0.4:
        reasons.append("temporal inconsistencies")
    elif temporal_score > 0.7:
        reasons.append("stable temporal patterns")
    
    if not reasons:
        reasons.append("mixed signals across analysis")
    
    reason = "; ".join(reasons).capitalize()
    
    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason
    }
