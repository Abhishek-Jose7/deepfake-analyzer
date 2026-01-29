"""
Adversarial Robustness Testing Module
Tests detection under various degradation conditions
"""
import cv2
import numpy as np
from copy import deepcopy


def add_compression_artifacts(frame, quality=50):
    """
    Simulate JPEG compression
    
    Args:
        frame: Input frame
        quality: JPEG quality (0-100, lower = more compression)
        
    Returns:
        Compressed frame
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded = cv2.imencode('.jpg', frame, encode_param)
    compressed = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    return compressed


def add_gaussian_noise(frame, sigma=25):
    """
    Add Gaussian noise
    
    Args:
        frame: Input frame
        sigma: Noise standard deviation
        
    Returns:
        Noisy frame
    """
    noise = np.random.normal(0, sigma, frame.shape).astype(np.float32)
    noisy = frame.astype(np.float32) + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


def add_blur(frame, kernel_size=5):
    """
    Add Gaussian blur
    
    Args:
        frame: Input frame
        kernel_size: Blur kernel size (odd number)
        
    Returns:
        Blurred frame
    """
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)


def resize_and_upscale(frame, scale=0.5):
    """
    Downscale then upscale (simulates low resolution)
    
    Args:
        frame: Input frame
        scale: Downscale factor (0-1)
        
    Returns:
        Degraded frame
    """
    h, w = frame.shape[:2]
    small = cv2.resize(frame, (int(w * scale), int(h * scale)))
    restored = cv2.resize(small, (w, h))
    return restored


def crop_and_pad(frame, crop_percent=0.2):
    """
    Crop edges and pad back (simulates cropping)
    
    Args:
        frame: Input frame
        crop_percent: Percentage to crop from each edge
        
    Returns:
        Cropped and padded frame
    """
    h, w = frame.shape[:2]
    crop_h = int(h * crop_percent)
    crop_w = int(w * crop_percent)
    
    cropped = frame[crop_h:h-crop_h, crop_w:w-crop_w]
    padded = cv2.resize(cropped, (w, h))
    
    return padded


def add_color_shift(frame, shift_amount=20):
    """
    Add color channel shift
    
    Args:
        frame: Input frame
        shift_amount: Amount to shift RGB channels
        
    Returns:
        Color-shifted frame
    """
    b, g, r = cv2.split(frame)
    
    b = np.clip(b.astype(np.int16) + np.random.randint(-shift_amount, shift_amount), 0, 255).astype(np.uint8)
    g = np.clip(g.astype(np.int16) + np.random.randint(-shift_amount, shift_amount), 0, 255).astype(np.uint8)
    r = np.clip(r.astype(np.int16) + np.random.randint(-shift_amount, shift_amount), 0, 255).astype(np.uint8)
    
    return cv2.merge([b, g, r])


def apply_adversarial_attack(frames, attack_type='compression', intensity='medium'):
    """
    Apply adversarial attack to frames
    
    Args:
        frames: List of frames
        attack_type: Type of attack ('compression', 'noise', 'blur', 'resolution', 'crop', 'color')
        intensity: Attack intensity ('low', 'medium', 'high')
        
    Returns:
        Attacked frames
    """
    intensity_params = {
        'compression': {'low': 80, 'medium': 50, 'high': 20},
        'noise': {'low': 10, 'medium': 25, 'high': 50},
        'blur': {'low': 3, 'medium': 5, 'high': 9},
        'resolution': {'low': 0.8, 'medium': 0.5, 'high': 0.3},
        'crop': {'low': 0.1, 'medium': 0.2, 'high': 0.35},
        'color': {'low': 10, 'medium': 20, 'high': 40}
    }
    
    param = intensity_params[attack_type][intensity]
    attacked_frames = []
    
    for frame in frames:
        if attack_type == 'compression':
            attacked = add_compression_artifacts(frame, param)
        elif attack_type == 'noise':
            attacked = add_gaussian_noise(frame, param)
        elif attack_type == 'blur':
            attacked = add_blur(frame, param)
        elif attack_type == 'resolution':
            attacked = resize_and_upscale(frame, param)
        elif attack_type == 'crop':
            attacked = crop_and_pad(frame, param)
        elif attack_type == 'color':
            attacked = add_color_shift(frame, param)
        else:
            attacked = frame
        
        attacked_frames.append(attacked)
    
    return attacked_frames


def test_robustness(frames, analyze_function):
    """
    Test robustness against multiple attacks
    
    Args:
        frames: Original frames
        analyze_function: Function to analyze frames (returns trust score)
        
    Returns:
        Robustness test results
    """
    attacks = [
        ('compression', 'low'),
        ('compression', 'medium'),
        ('compression', 'high'),
        ('noise', 'medium'),
        ('blur', 'medium'),
        ('resolution', 'medium'),
        ('crop', 'medium'),
    ]
    
    results = {
        'original': analyze_function(frames),
        'attacks': {}
    }
    
    for attack_type, intensity in attacks:
        attacked_frames = apply_adversarial_attack(frames, attack_type, intensity)
        score = analyze_function(attacked_frames)
        
        attack_name = f"{attack_type}_{intensity}"
        results['attacks'][attack_name] = {
            'score': score,
            'degradation': abs(results['original'] - score)
        }
    
    return results
