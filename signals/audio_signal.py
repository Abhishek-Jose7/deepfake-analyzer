"""
Audio Signal Wrapper
"""
from signals.audio import analyze_audio as _analyze_audio


def analyze_audio(audio_path):
    """
    Analyze audio signals from audio file
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dictionary with score and confidence
    """
    if audio_path is None:
        return {"score": 0.5, "confidence": 0.0}
    
    result = _analyze_audio(audio_path)
    
    return {
        "score": result.get("combined", 0.5),
        "confidence": 0.8 if result.get("combined", 0.5) != 0.5 else 0.0
    }
