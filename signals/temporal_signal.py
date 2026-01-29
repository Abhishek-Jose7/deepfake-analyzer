"""
Temporal Signal Wrapper
"""
from signals.temporal import analyze_temporal_signals


def analyze_temporal(frames):
    """
    Analyze temporal signals from frames
    
    Args:
        frames: List of video frames
        
    Returns:
        Dictionary with score and confidence
    """
    if len(frames) < 2:
        return {"score": 0.5, "confidence": 0.0}
    
    result = analyze_temporal_signals(frames)
    
    # Calculate confidence based on number of frames
    confidence = min(1.0, len(frames) / 30) if result.get("combined", 0.5) != 0.5 else 0.0
    
    return {
        "score": result.get("combined", 0.5),
        "confidence": confidence
    }
