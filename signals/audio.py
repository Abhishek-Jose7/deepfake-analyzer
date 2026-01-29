"""
Audio signal detection for deepfake voices
Uses spectral analysis to detect synthetic audio
"""
import numpy as np


def audio_score(audio_path):
    """
    Analyze audio for synthetic characteristics
    
    Uses spectral flatness - synthetic audio (TTS) often has 
    flatter spectral characteristics than natural speech.
    
    Args:
        audio_path: Path to audio file (WAV format)
        
    Returns:
        Score between 0 and 1 (higher = more natural)
    """
    if audio_path is None:
        return 0.5  # Ambiguous if no audio
    
    try:
        import librosa
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate spectral flatness
        flatness = np.mean(librosa.feature.spectral_flatness(y=y))
        
        # Synthetic audio often has higher flatness (0.3-0.7)
        # Natural speech typically has lower flatness (0.05-0.2)
        score = 1.0 - flatness
        score = max(0.0, min(score, 1.0))
        
        return score
        
    except Exception as e:
        # If analysis fails, return ambiguous score
        return 0.5


def spectral_rolloff_score(audio_path):
    """
    Analyze spectral rolloff characteristics
    
    Deepfake audio often has different energy distribution
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Score between 0 and 1
    """
    if audio_path is None:
        return 0.5
    
    try:
        import librosa
        
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate spectral rolloff
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        
        # Normalize by Nyquist frequency
        normalized_rolloff = np.mean(rolloff) / (sr / 2)
        
        # Real speech typically has rolloff around 0.85
        # Synthetic may be lower or higher
        deviation = abs(normalized_rolloff - 0.85)
        score = 1.0 - min(1.0, deviation * 2)
        
        return score
        
    except Exception:
        return 0.5


def zero_crossing_rate_score(audio_path):
    """
    Analyze zero crossing rate
    
    Synthetic voices may have different zero crossing patterns
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Score between 0 and 1
    """
    if audio_path is None:
        return 0.5
    
    try:
        import librosa
        
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)
        mean_zcr = np.mean(zcr)
        
        # Natural speech typically has ZCR around 0.05-0.15
        if 0.05 <= mean_zcr <= 0.15:
            score = 1.0
        elif mean_zcr < 0.05:
            score = mean_zcr / 0.05
        else:
            score = max(0.0, 1.0 - (mean_zcr - 0.15) / 0.15)
        
        return score
        
    except Exception:
        return 0.5


def analyze_audio(audio_path):
    """
    Comprehensive audio analysis
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dictionary with audio scores
    """
    if audio_path is None:
        return {
            'flatness': 0.5,
            'rolloff': 0.5,
            'zcr': 0.5,
            'combined': 0.5
        }
    
    flatness = audio_score(audio_path)
    rolloff = spectral_rolloff_score(audio_path)
    zcr = zero_crossing_rate_score(audio_path)
    
    # Weighted combination
    combined = 0.5 * flatness + 0.3 * rolloff + 0.2 * zcr
    
    return {
        'flatness': flatness,
        'rolloff': rolloff,
        'zcr': zcr,
        'combined': combined
    }
