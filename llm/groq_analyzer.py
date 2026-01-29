"""
Groq LLM Integration for DeepTrust
Uses Llama 3.2 Vision for intelligent deepfake analysis
"""
import os
import base64
import json
from typing import Optional, List, Dict, Any


def encode_image_to_base64(image_data) -> str:
    """
    Encode image bytes or numpy array to base64
    
    Args:
        image_data: Image as bytes or numpy array
        
    Returns:
        Base64 encoded string
    """
    import cv2
    import numpy as np
    
    if isinstance(image_data, np.ndarray):
        # Convert numpy array to JPEG bytes
        _, buffer = cv2.imencode('.jpg', image_data, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        image_bytes = buffer.tobytes()
    else:
        image_bytes = image_data
    
    return base64.b64encode(image_bytes).decode('utf-8')


class GroqAnalyzer:
    """
    Groq API client for Llama 3.2 Vision analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.2-90b-vision-preview"  # Llama 3.2 Vision
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            print("⚠️ GROQ_API_KEY not set - LLM analysis disabled")
    
    def analyze_frames(self, frames: List, signal_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze video frames using Llama 3.2 Vision
        
        Args:
            frames: List of video frames (numpy arrays)
            signal_scores: Dictionary of signal analysis scores
            
        Returns:
            LLM analysis results
        """
        if not self.enabled:
            return {
                "enabled": False,
                "reason": "Groq API key not configured"
            }
        
        if not frames:
            return {
                "enabled": True,
                "error": "No frames provided"
            }
        
        try:
            import requests
            
            # Select key frames for analysis (beginning, middle, end)
            num_frames = len(frames)
            if num_frames >= 3:
                selected_indices = [0, num_frames // 2, num_frames - 1]
            else:
                selected_indices = list(range(num_frames))
            
            # Encode frames to base64
            encoded_frames = []
            for idx in selected_indices[:3]:  # Max 3 frames
                encoded = encode_image_to_base64(frames[idx])
                encoded_frames.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded}"
                    }
                })
            
            # Build the prompt
            prompt = self._build_analysis_prompt(signal_scores)
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert forensic analyst specializing in detecting manipulated media and deepfakes. 
                    
Your task is to analyze video frames for signs of manipulation. Look for:
1. Facial inconsistencies (unnatural skin texture, blurring around edges)
2. Lighting anomalies (shadows that don't match light sources)
3. Temporal artifacts (if comparing frames - jitter, flickering)
4. Background inconsistencies
5. Eye and mouth region abnormalities
6. Compression artifacts that suggest re-encoding

Be objective and scientific in your analysis. If you cannot determine authenticity, say so clearly.
Always provide a confidence level (high/medium/low) for your assessment."""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *encoded_frames
                    ]
                }
            ]
            
            # Call Groq API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.3  # Lower temperature for more consistent analysis
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                return {
                    "enabled": True,
                    "error": f"API error: {error_detail}",
                    "status_code": response.status_code
                }
            
            result = response.json()
            llm_response = result["choices"][0]["message"]["content"]
            
            # Parse the response
            parsed = self._parse_llm_response(llm_response)
            
            return {
                "enabled": True,
                "model": self.model,
                "analysis": llm_response,
                "parsed": parsed,
                "frames_analyzed": len(selected_indices)
            }
            
        except requests.exceptions.Timeout:
            return {
                "enabled": True,
                "error": "API request timed out"
            }
        except Exception as e:
            return {
                "enabled": True,
                "error": str(e)
            }
    
    def _build_analysis_prompt(self, signal_scores: Dict[str, float]) -> str:
        """Build the analysis prompt with signal context"""
        
        vision_score = signal_scores.get("vision", 0.5)
        audio_score = signal_scores.get("audio", 0.5)
        temporal_score = signal_scores.get("temporal", 0.5)
        
        context = f"""Analyze these video frames for signs of deepfake manipulation.

SIGNAL ANALYSIS CONTEXT:
- Vision Signal Score: {vision_score:.2f} (1.0 = authentic, 0.0 = fake)
- Audio Signal Score: {audio_score:.2f}
- Temporal Signal Score: {temporal_score:.2f}

Based on the images and the signal analysis above, provide:

1. **Visual Assessment**: What do you observe in the frames? Any signs of manipulation?

2. **Specific Artifacts**: List any specific artifacts you detect (e.g., blurring, inconsistent lighting, unnatural textures)

3. **Confidence**: Your confidence in your assessment (HIGH/MEDIUM/LOW)

4. **Verdict**: Your conclusion - is this likely AUTHENTIC, MANIPULATED, or UNCERTAIN?

5. **Reasoning**: Brief explanation of your reasoning

Please be precise and factual. If the quality is too low to assess, say so."""
        
        return context
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to extract structured data"""
        
        parsed = {
            "confidence": "medium",
            "verdict": "uncertain",
            "artifacts_detected": [],
            "reasoning": ""
        }
        
        response_lower = response.lower()
        
        # Extract confidence
        if "high" in response_lower and "confidence" in response_lower:
            parsed["confidence"] = "high"
        elif "low" in response_lower and "confidence" in response_lower:
            parsed["confidence"] = "low"
        
        # Extract verdict
        if "authentic" in response_lower or "real" in response_lower:
            if "not authentic" in response_lower or "not real" in response_lower:
                parsed["verdict"] = "manipulated"
            else:
                parsed["verdict"] = "authentic"
        elif "manipulated" in response_lower or "fake" in response_lower or "deepfake" in response_lower:
            if "not manipulated" in response_lower or "not fake" in response_lower:
                parsed["verdict"] = "authentic"
            else:
                parsed["verdict"] = "manipulated"
        
        # Extract common artifacts
        artifact_keywords = [
            "blurring", "blur", "distortion", "artifacts", "inconsistent",
            "unnatural", "smoothing", "compression", "flickering", "jitter"
        ]
        for keyword in artifact_keywords:
            if keyword in response_lower:
                parsed["artifacts_detected"].append(keyword)
        
        # Extract reasoning (last paragraph or sentence with "because"/"since")
        sentences = response.split('.')
        for sentence in sentences:
            if any(word in sentence.lower() for word in ["because", "since", "therefore", "indicates"]):
                parsed["reasoning"] = sentence.strip() + "."
                break
        
        if not parsed["reasoning"] and sentences:
            parsed["reasoning"] = sentences[-1].strip() + "."
        
        return parsed
    
    def generate_explanation(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a human-readable explanation based on analysis
        
        Args:
            analysis_result: Full analysis result dictionary
            
        Returns:
            Human-readable explanation string
        """
        if not self.enabled:
            return self._generate_fallback_explanation(analysis_result)
        
        try:
            import requests
            
            trust_score = analysis_result.get("trust_score", 0.5)
            decision = analysis_result.get("decision", "Unknown")
            signals = analysis_result.get("signals", {})
            
            prompt = f"""Based on this deepfake analysis, write a brief, clear explanation for a non-technical user:

Trust Score: {trust_score:.1%}
Decision: {decision}
Vision Signal: {signals.get('vision', {}).get('score', 0.5):.1%}
Audio Signal: {signals.get('audio', {}).get('score', 0.5):.1%}
Temporal Signal: {signals.get('temporal', {}).get('score', 0.5):.1%}

Write 2-3 sentences explaining what this means and why. Be clear and avoid jargon."""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-8b-instant",  # Use smaller model for text-only
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 256,
                "temperature": 0.5
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return self._generate_fallback_explanation(analysis_result)
                
        except Exception:
            return self._generate_fallback_explanation(analysis_result)
    
    def _generate_fallback_explanation(self, analysis_result: Dict[str, Any]) -> str:
        """Generate explanation without LLM"""
        
        trust_score = analysis_result.get("trust_score", 0.5)
        decision = analysis_result.get("decision", "Unknown")
        signals = analysis_result.get("signals", {})
        
        vision = signals.get("vision", {}).get("score", 0.5)
        audio = signals.get("audio", {}).get("score", 0.5)
        temporal = signals.get("temporal", {}).get("score", 0.5)
        
        parts = []
        
        if trust_score >= 0.7:
            parts.append(f"This video appears to be authentic with a {trust_score:.0%} trust score.")
        elif trust_score >= 0.4:
            parts.append(f"This video shows mixed signals with a {trust_score:.0%} trust score.")
        else:
            parts.append(f"This video shows signs of manipulation with a {trust_score:.0%} trust score.")
        
        # Add signal-specific insights
        issues = []
        if vision < 0.4:
            issues.append("visual artifacts detected")
        if audio < 0.4:
            issues.append("synthetic audio patterns")
        if temporal < 0.4:
            issues.append("temporal inconsistencies")
        
        if issues:
            parts.append(f"Key concerns: {', '.join(issues)}.")
        elif trust_score >= 0.7:
            parts.append("All signals indicate authentic content.")
        
        return " ".join(parts)


# Global instance
groq_analyzer = GroqAnalyzer()
