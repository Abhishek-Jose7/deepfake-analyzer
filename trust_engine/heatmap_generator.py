"""
Heatmap Generator for Visual Explainability
Generates visual heatmaps showing suspicious regions in frames
"""
import cv2
import numpy as np
import base64


def generate_artifact_heatmap(frame):
    """
    Generate heatmap showing regions with high artifacts
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Heatmap overlay image
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate local Laplacian variance in sliding windows
    h, w = gray.shape
    window_size = 32
    stride = 16
    
    heatmap = np.zeros((h, w), dtype=np.float32)
    
    for y in range(0, h - window_size, stride):
        for x in range(0, w - window_size, stride):
            window = gray[y:y+window_size, x:x+window_size]
            lap = cv2.Laplacian(window, cv2.CV_64F)
            variance = lap.var()
            
            # Lower variance = more suspicious
            suspicion = max(0, 1.0 - (variance / 1000))
            heatmap[y:y+window_size, x:x+window_size] = np.maximum(
                heatmap[y:y+window_size, x:x+window_size],
                suspicion
            )
    
    # Normalize and apply colormap
    heatmap = (heatmap * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Blend with original
    overlay = cv2.addWeighted(frame, 0.6, heatmap_colored, 0.4, 0)
    
    return overlay, heatmap


def generate_edge_heatmap(frame):
    """
    Generate heatmap showing edge inconsistencies
    
    Args:
        frame: Input frame (BGR format)
        
    Returns:
        Edge heatmap overlay
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(gray, 100, 200)
    
    # Dilate to show edge regions
    kernel = np.ones((5, 5), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=2)
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(edges_dilated, cv2.COLORMAP_HOT)
    
    # Blend
    overlay = cv2.addWeighted(frame, 0.7, heatmap_colored, 0.3, 0)
    
    return overlay, edges_dilated


def generate_temporal_heatmap(frames, frame_idx):
    """
    Generate heatmap showing temporal inconsistencies
    
    Args:
        frames: List of frames
        frame_idx: Index of frame to analyze
        
    Returns:
        Temporal inconsistency heatmap
    """
    if frame_idx == 0 or frame_idx >= len(frames):
        return frames[frame_idx], np.zeros(frames[frame_idx].shape[:2], dtype=np.uint8)
    
    current = frames[frame_idx]
    previous = frames[frame_idx - 1]
    
    # Calculate absolute difference
    diff = cv2.absdiff(current, previous)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Threshold and enhance
    _, diff_thresh = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(diff_thresh, cv2.COLORMAP_RAINBOW)
    
    # Blend
    overlay = cv2.addWeighted(current, 0.7, heatmap_colored, 0.3, 0)
    
    return overlay, diff_thresh


def generate_composite_heatmap(frame, frames=None, frame_idx=0):
    """
    Generate composite heatmap combining multiple signals
    
    Args:
        frame: Current frame
        frames: List of all frames (optional, for temporal)
        frame_idx: Current frame index
        
    Returns:
        Dictionary with all heatmaps
    """
    artifact_overlay, artifact_map = generate_artifact_heatmap(frame)
    edge_overlay, edge_map = generate_edge_heatmap(frame)
    
    result = {
        'artifact': {
            'overlay': artifact_overlay,
            'map': artifact_map
        },
        'edge': {
            'overlay': edge_overlay,
            'map': edge_map
        }
    }
    
    # Add temporal if available
    if frames is not None and frame_idx > 0:
        temporal_overlay, temporal_map = generate_temporal_heatmap(frames, frame_idx)
        result['temporal'] = {
            'overlay': temporal_overlay,
            'map': temporal_map
        }
    
    return result


def frame_to_base64(frame):
    """
    Convert frame to base64 for embedding in HTML/PDF
    
    Args:
        frame: OpenCV frame
        
    Returns:
        Base64 encoded string
    """
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"
