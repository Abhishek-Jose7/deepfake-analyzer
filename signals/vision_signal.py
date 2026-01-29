"""
Vision Signal Wrapper
"""
from signals.vision import analyze_frames


def analyze_vision(frames):
    """
    Analyze vision signals from frames
    
    Args:
        frames: List of video frames
        
    Returns:
        Dictionary with score and confidence
    """
    if not frames:
        return {"score": 0.5, "confidence": 0.0}
    
    combined_score = analyze_frames(frames)
    
    # Calculate confidence based on number of frames
    confidence = min(1.0, len(frames) / 30)
    
    return {
        "score": combined_score,
        "confidence": confidence
    }
