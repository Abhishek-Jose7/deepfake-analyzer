"""
DeepTrust Model Package
"""
from model.detector import DeepfakeDetector, create_model, LABELS, LABEL_TO_IDX
from model.inference import DeepfakeInference, get_inference_engine, analyze_video, analyze_frames

__all__ = [
    'DeepfakeDetector',
    'create_model',
    'LABELS',
    'LABEL_TO_IDX',
    'DeepfakeInference',
    'get_inference_engine',
    'analyze_video',
    'analyze_frames'
]
