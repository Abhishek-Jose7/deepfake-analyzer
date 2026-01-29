"""
Audio utilities for extraction and processing
"""
import subprocess
import os
import tempfile


def extract_audio(video_path):
    """
    Extract audio from video file using ffmpeg
    
    Args:
        video_path: Path to video file
        
    Returns:
        Path to extracted audio file (WAV format)
    """
    # Create temporary file for audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    audio_path = temp_audio.name
    temp_audio.close()
    
    try:
        # Use ffmpeg to extract audio
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM codec
            '-ar', '44100',  # Sample rate
            '-ac', '2',  # Stereo
            '-y',  # Overwrite
            audio_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return audio_path
        
    except subprocess.CalledProcessError as e:
        # If ffmpeg fails, return None
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return None
    except FileNotFoundError:
        # ffmpeg not installed
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return None
