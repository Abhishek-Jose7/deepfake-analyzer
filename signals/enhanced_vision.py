"""
Enhanced Vision Analysis for Deepfake Detection
Uses multiple computer vision techniques for more accurate detection
"""
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple


class EnhancedVisionAnalyzer:
    """
    Advanced vision-based deepfake detection using multiple signals
    """
    
    def __init__(self):
        # Load face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        # Load eye detector for face region analysis
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
    
    def analyze_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive analysis of a single frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary with detailed analysis
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Laplacian variance (blur/sharpness detection)
        laplacian_score = self._laplacian_variance(gray)
        
        # 2. Edge consistency
        edge_score = self._edge_consistency(gray)
        
        # 3. Color distribution analysis
        color_score = self._color_distribution(frame)
        
        # 4. Noise pattern analysis
        noise_score = self._noise_analysis(gray)
        
        # 5. Face region analysis (if face detected)
        face_score, face_details = self._face_analysis(frame, gray)
        
        # 6. Compression artifact detection
        compression_score = self._compression_artifacts(gray)
        
        # 7. Frequency domain analysis
        frequency_score = self._frequency_analysis(gray)
        
        # Combine scores with weights
        weights = {
            'laplacian': 0.15,
            'edge': 0.15,
            'color': 0.1,
            'noise': 0.1,
            'face': 0.25,  # Higher weight for face analysis
            'compression': 0.1,
            'frequency': 0.15
        }
        
        combined_score = (
            laplacian_score * weights['laplacian'] +
            edge_score * weights['edge'] +
            color_score * weights['color'] +
            noise_score * weights['noise'] +
            face_score * weights['face'] +
            compression_score * weights['compression'] +
            frequency_score * weights['frequency']
        )
        
        return {
            'combined': combined_score,
            'laplacian': laplacian_score,
            'edge': edge_score,
            'color': color_score,
            'noise': noise_score,
            'face': face_score,
            'compression': compression_score,
            'frequency': frequency_score,
            'face_detected': face_details.get('detected', False),
            'face_count': face_details.get('count', 0)
        }
    
    def analyze_frames(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """
        Analyze multiple frames and aggregate results
        
        Args:
            frames: List of video frames
            
        Returns:
            Aggregated analysis with confidence
        """
        if not frames:
            return {
                'score': 0.5,
                'confidence': 0.0,
                'details': 'No frames to analyze'
            }
        
        # Analyze each frame
        frame_results = []
        for frame in frames:
            try:
                result = self.analyze_frame(frame)
                frame_results.append(result)
            except Exception as e:
                continue
        
        if not frame_results:
            return {
                'score': 0.5,
                'confidence': 0.0,
                'details': 'Frame analysis failed'
            }
        
        # Aggregate scores
        scores = [r['combined'] for r in frame_results]
        avg_score = np.mean(scores)
        std_score = np.std(scores)
        
        # Higher consistency = higher confidence
        consistency = 1.0 - min(1.0, std_score * 2)
        
        # Calculate confidence based on:
        # 1. Number of frames analyzed
        # 2. Consistency of scores
        # 3. Whether faces were detected
        frame_confidence = min(1.0, len(frame_results) / 20)
        face_detected = any(r.get('face_detected', False) for r in frame_results)
        face_confidence = 1.0 if face_detected else 0.7
        
        overall_confidence = frame_confidence * consistency * face_confidence
        
        # Detailed breakdown
        breakdown = {
            'laplacian': np.mean([r['laplacian'] for r in frame_results]),
            'edge': np.mean([r['edge'] for r in frame_results]),
            'color': np.mean([r['color'] for r in frame_results]),
            'noise': np.mean([r['noise'] for r in frame_results]),
            'face': np.mean([r['face'] for r in frame_results]),
            'compression': np.mean([r['compression'] for r in frame_results]),
            'frequency': np.mean([r['frequency'] for r in frame_results])
        }
        
        return {
            'score': avg_score,
            'confidence': overall_confidence,
            'consistency': consistency,
            'frames_analyzed': len(frame_results),
            'face_detected': face_detected,
            'breakdown': breakdown
        }
    
    def _laplacian_variance(self, gray: np.ndarray) -> float:
        """Detect blur/smoothing using Laplacian variance"""
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        variance = lap.var()
        
        # Normalize: real videos typically have variance 500-2000
        # Deepfakes often have lower variance due to smoothing
        if variance < 100:
            return 0.2  # Very smooth - suspicious
        elif variance < 300:
            return 0.4
        elif variance < 500:
            return 0.6
        elif variance < 1500:
            return 0.9  # Normal range
        else:
            return 0.7  # Very sharp - slightly unusual
    
    def _edge_consistency(self, gray: np.ndarray) -> float:
        """Analyze edge consistency"""
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate edge density
        edge_density = np.sum(edges > 0) / edges.size
        
        # Analyze edge sharpness
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        edge_strength = np.mean(magnitude)
        
        # Normal edge density is 0.05-0.2
        density_score = 1.0 if 0.05 <= edge_density <= 0.2 else 0.7
        
        # Normal edge strength is 10-50
        strength_score = 1.0 if 10 <= edge_strength <= 50 else 0.7
        
        return (density_score + strength_score) / 2
    
    def _color_distribution(self, frame: np.ndarray) -> float:
        """Analyze color distribution for anomalies"""
        # Convert to LAB for better color analysis
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Check for unnatural color uniformity
        a_std = np.std(a)
        b_std = np.std(b)
        
        # Natural images have more color variation
        if a_std < 5 or b_std < 5:
            return 0.4  # Very uniform - suspicious
        elif a_std < 15 or b_std < 15:
            return 0.7
        else:
            return 0.9
    
    def _noise_analysis(self, gray: np.ndarray) -> float:
        """Analyze noise patterns"""
        # Estimate noise using local variance
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = gray.astype(float) - blur.astype(float)
        noise_std = np.std(noise)
        
        # Natural videos have consistent noise patterns
        # GAN-generated content often has different noise characteristics
        if noise_std < 2:
            return 0.4  # Very little noise - possibly over-processed
        elif noise_std > 20:
            return 0.6  # Too much noise
        else:
            return 0.9
    
    def _face_analysis(self, frame: np.ndarray, gray: np.ndarray) -> Tuple[float, Dict]:
        """Analyze face regions for manipulation artifacts"""
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return 0.5, {'detected': False, 'count': 0}
        
        face_scores = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            face_color = frame[y:y+h, x:x+w]
            
            # 1. Check face region blur
            face_lap = cv2.Laplacian(face_roi, cv2.CV_64F).var()
            
            # 2. Check boundary sharpness (deepfakes often have soft boundaries)
            boundary_region = gray[max(0,y-5):y+h+5, max(0,x-5):x+w+5]
            boundary_edges = cv2.Canny(boundary_region, 50, 150)
            boundary_density = np.sum(boundary_edges > 0) / boundary_edges.size
            
            # 3. Check for unnatural skin smoothness
            skin_smoothness = np.std(face_roi)
            
            # 4. Eye detection (deepfakes sometimes have eye issues)
            eyes = self.eye_cascade.detectMultiScale(face_roi)
            has_valid_eyes = len(eyes) >= 2
            
            # Score face
            blur_score = min(1.0, face_lap / 500)
            boundary_score = 1.0 if boundary_density > 0.05 else 0.6
            smoothness_score = 1.0 if skin_smoothness > 20 else 0.5
            eye_score = 1.0 if has_valid_eyes else 0.7
            
            face_score = (blur_score * 0.3 + boundary_score * 0.3 + 
                         smoothness_score * 0.2 + eye_score * 0.2)
            face_scores.append(face_score)
        
        return np.mean(face_scores), {'detected': True, 'count': len(faces)}
    
    def _compression_artifacts(self, gray: np.ndarray) -> float:
        """Detect double compression artifacts"""
        h, w = gray.shape
        block_size = 8
        
        # Analyze 8x8 block boundaries (JPEG/H.264 use 8x8 blocks)
        boundary_diffs = []
        
        for i in range(block_size, h - block_size, block_size):
            row_diff = np.mean(np.abs(
                gray[i-1, :].astype(float) - gray[i, :].astype(float)
            ))
            boundary_diffs.append(row_diff)
        
        for j in range(block_size, w - block_size, block_size):
            col_diff = np.mean(np.abs(
                gray[:, j-1].astype(float) - gray[:, j].astype(float)
            ))
            boundary_diffs.append(col_diff)
        
        if not boundary_diffs:
            return 0.5
        
        avg_boundary_diff = np.mean(boundary_diffs)
        
        # High boundary differences indicate compression artifacts
        # Double compression (re-encoding) creates stronger artifacts
        if avg_boundary_diff > 15:
            return 0.4  # Strong artifacts - suspicious
        elif avg_boundary_diff > 8:
            return 0.7
        else:
            return 0.9
    
    def _frequency_analysis(self, gray: np.ndarray) -> float:
        """Analyze frequency domain for GAN artifacts"""
        # Apply FFT
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude = np.abs(fshift)
        
        # Normalize
        magnitude = np.log1p(magnitude)
        magnitude = magnitude / np.max(magnitude)
        
        # GANs often produce specific frequency patterns
        # Check for unusual frequency concentrations
        h, w = magnitude.shape
        center_h, center_w = h // 2, w // 2
        
        # Analyze high-frequency region
        high_freq = magnitude[center_h-10:center_h+10, center_w-10:center_w+10]
        high_freq_ratio = np.mean(high_freq)
        
        # Natural images have more distributed high frequencies
        if high_freq_ratio > 0.8:
            return 0.5  # Unusual concentration
        else:
            return 0.9


# Global instance
enhanced_vision = EnhancedVisionAnalyzer()


def analyze_vision(frames: List[np.ndarray]) -> Dict[str, Any]:
    """
    Main entry point for vision analysis
    
    Args:
        frames: List of video frames
        
    Returns:
        Analysis results dictionary
    """
    return enhanced_vision.analyze_frames(frames)
