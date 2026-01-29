"""
Trust Scoring Engine - The Brain
Combines weak signals intelligently with quality-aware confidence calibration
"""


def trust_score(vision, audio, temporal, quality):
    """
    Calculate trust score with intelligent signal combination
    
    This is NOT a simple average. We adjust confidence based on input quality
    and provide human-readable explanations.
    
    Args:
        vision: Vision signal score (0-1)
        audio: Audio signal score (0-1)
        temporal: Temporal signal score (0-1)
        quality: Overall quality score (0-1)
        
    Returns:
        Tuple of (trust_score, decision, reason)
    """
    # Base weights for different signals
    weights = {
        "vision": 0.4,
        "audio": 0.3,
        "temporal": 0.3
    }
    
    # Calculate raw score
    raw_score = (
        vision * weights["vision"] +
        audio * weights["audio"] +
        temporal * weights["temporal"]
    )
    
    # Quality-based confidence adjustment
    if quality < 0.3:
        # Very poor quality - drastically reduce confidence
        adjusted_score = raw_score * 0.4
        decision = "Ambiguous"
        reason = "Very Low Quality Input - Cannot Make Reliable Assessment"
        
    elif quality < 0.5:
        # Poor quality - reduce confidence
        adjusted_score = raw_score * 0.6
        decision = "Ambiguous"
        reason = "Low Quality Input - Limited Confidence"
        
    elif quality < 0.7:
        # Moderate quality - slight reduction
        adjusted_score = raw_score * 0.85
        
        if adjusted_score > 0.65:
            decision = "Likely Real"
            reason = "Moderate Quality - Signals Indicate Real Content"
        elif adjusted_score < 0.35:
            decision = "Likely Fake"
            reason = "Moderate Quality - Multiple Suspicious Signals"
        else:
            decision = "Ambiguous"
            reason = "Moderate Quality - Mixed Signals"
            
    else:
        # Good quality - full confidence
        adjusted_score = raw_score
        
        if adjusted_score > 0.7:
            decision = "Real"
            reason = "High Quality Input - Strong Real Signals"
        elif adjusted_score < 0.3:
            decision = "Fake"
            reason = "High Quality Input - Strong Deepfake Signals"
        elif adjusted_score > 0.55:
            decision = "Likely Real"
            reason = "Good Quality - Signals Lean Toward Real"
        elif adjusted_score < 0.45:
            decision = "Likely Fake"
            reason = "Good Quality - Signals Lean Toward Fake"
        else:
            decision = "Ambiguous"
            reason = "Good Quality - Balanced Signals, Cannot Determine"
    
    # Add specific signal insights to reason
    signal_insights = []
    
    if temporal < 0.4:
        signal_insights.append("high temporal inconsistency")
    if vision < 0.4:
        signal_insights.append("visual artifacts detected")
    if audio < 0.4:
        signal_insights.append("synthetic audio characteristics")
    
    if signal_insights:
        reason += f" ({', '.join(signal_insights)})"
    
    return adjusted_score, decision, reason


def generate_report(vision_data, audio_data, temporal_data, quality_data, final_score, decision, reason):
    """
    Generate comprehensive analysis report
    
    Args:
        vision_data: Dictionary with vision analysis
        audio_data: Dictionary with audio analysis
        temporal_data: Dictionary with temporal analysis
        quality_data: Dictionary with quality analysis
        final_score: Final trust score
        decision: Trust decision
        reason: Explanation
        
    Returns:
        Dictionary with complete report
    """
    report = {
        "trust_score": round(final_score, 2),
        "decision": decision,
        "reason": reason,
        "signals": {
            "vision": {
                "score": round(vision_data.get('combined', 0.5), 2),
                "artifact_detection": round(vision_data.get('artifact_score', 0.5), 2),
                "edge_consistency": round(vision_data.get('edge_consistency', 0.5), 2)
            },
            "audio": {
                "score": round(audio_data.get('combined', 0.5), 2),
                "spectral_flatness": round(audio_data.get('flatness', 0.5), 2),
                "spectral_rolloff": round(audio_data.get('rolloff', 0.5), 2),
                "zero_crossing_rate": round(audio_data.get('zcr', 0.5), 2)
            },
            "temporal": {
                "score": round(temporal_data.get('combined', 0.5), 2),
                "consistency": round(temporal_data.get('consistency', 0.5), 2),
                "variance": round(temporal_data.get('variance', 0.5), 2),
                "optical_flow": round(temporal_data.get('optical_flow', 0.5), 2)
            }
        },
        "quality_assessment": {
            "overall": round(quality_data.get('overall', 0.5), 2),
            "compression": round(quality_data.get('compression', 0.5), 2),
            "blocking_artifacts": round(quality_data.get('blocking', 0.5), 2),
            "noise_level": round(quality_data.get('noise', 0.5), 2),
            "resolution": round(quality_data.get('resolution', 0.5), 2)
        }
    }
    
    return report
