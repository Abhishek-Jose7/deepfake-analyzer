"""
Educational Dashboard Module
Provides educational content about deepfakes based on analysis results
"""


DEEPFAKE_STATS = {
    'global_incidents': {
        '2023': 95820,
        '2024': 143000,
        'growth_rate': '49.2%'
    },
    'detection_accuracy': {
        'human_detection': '0.54',
        'ai_detection': '0.82',
        'hybrid_approach': '0.91'
    },
    'common_targets': [
        {'category': 'Political Figures', 'percentage': 42},
        {'category': 'Celebrities', 'percentage': 31},
        {'category': 'General Public', 'percentage': 27}
    ],
    'generation_methods': [
        {'method': 'GAN-based (StyleGAN, etc.)', 'prevalence': 38},
        {'method': 'Face Swap (DeepFaceLab)', 'prevalence': 29},
        {'method': 'Face Reenactment (First Order Motion)', 'prevalence': 21},
        {'method': 'Audio Synthesis (TTS)', 'prevalence': 12}
    ]
}


SIGNAL_EXPLANATIONS = {
    'vision': {
        'high': {
            'title': 'Strong Visual Authenticity',
            'explanation': 'The video shows natural texture details and consistent edge patterns. Real videos typically have high-frequency noise from camera sensors and natural skin texture.',
            'indicators': [
                'Consistent Laplacian variance across frames',
                'Natural edge transitions',
                'Appropriate skin texture detail',
                'No signs of over-smoothing'
            ]
        },
        'low': {
            'title': 'Visual Artifacts Detected',
            'explanation': 'The analysis found suspicious visual patterns. Deepfake generators often over-smooth faces to hide artifacts, reducing natural texture variance.',
            'indicators': [
                'Unnaturally smooth skin regions',
                'Inconsistent edge patterns',
                'Low Laplacian variance',
                'Possible GAN fingerprints'
            ]
        }
    },
    'audio': {
        'high': {
            'title': 'Natural Voice Characteristics',
            'explanation': 'The audio exhibits characteristics of natural human speech, including appropriate spectral distribution and energy patterns.',
            'indicators': [
                'Natural spectral flatness (0.05-0.2)',
                'Appropriate spectral rolloff',
                'Normal zero crossing rate',
                'Consistent formant structure'
            ]
        },
        'low': {
            'title': 'Synthetic Audio Detected',
            'explanation': 'The voice shows characteristics common in text-to-speech systems or voice cloning technology.',
            'indicators': [
                'Unusually flat spectral characteristics',
                'Abnormal zero crossing patterns',
                'Missing micro-variations in pitch',
                'Unnatural prosody'
            ]
        }
    },
    'temporal': {
        'high': {
            'title': 'Consistent Temporal Flow',
            'explanation': 'Frame-to-frame analysis shows natural progression and motion. Real videos have consistent temporal patterns.',
            'indicators': [
                'Smooth frame transitions',
                'Consistent motion vectors',
                'Stable optical flow',
                'Natural temporal variance'
            ]
        },
        'low': {
            'title': 'Temporal Inconsistencies',
            'explanation': 'Significant frame-to-frame instabilities detected. Deepfakes often process frames independently, creating temporal artifacts.',
            'indicators': [
                'Erratic frame differences',
                'Inconsistent optical flow',
                'Sudden facial feature shifts',
                'Motion discontinuities'
            ]
        }
    },
    'quality': {
        'high': {
            'title': 'High Quality Input',
            'explanation': 'The video quality is sufficient for reliable analysis. All detection signals can operate at full confidence.',
            'indicators': [
                'Minimal compression artifacts',
                'Adequate resolution',
                'Low noise levels',
                'Clean edges'
            ]
        },
        'low': {
            'title': 'Degraded Input Quality',
            'explanation': 'Heavy compression, low resolution, or noise limits analysis reliability. The system has reduced confidence accordingly.',
            'indicators': [
                'Heavy JPEG/H.264 compression',
                'Low resolution',
                'High noise levels',
                'Blocking artifacts'
            ]
        }
    }
}


DETECTION_TIPS = [
    {
        'title': 'Watch for Unnatural Blinking',
        'description': 'Early deepfakes had irregular blinking patterns. While modern ones improved, watch for unnaturally slow or absent blinks.',
        'difficulty': 'Easy'
    },
    {
        'title': 'Check Facial Boundaries',
        'description': 'Look at where the face meets hair, ears, or background. Deepfakes often blur these boundaries unnaturally.',
        'difficulty': 'Medium'
    },
    {
        'title': 'Analyze Lip Sync',
        'description': 'Does the mouth movement perfectly match the words? Perfect sync can indicate synthesis, as natural speech has micro-delays.',
        'difficulty': 'Medium'
    },
    {
        'title': 'Observe Lighting Consistency',
        'description': 'Check if lighting on the face matches the environment. Deepfakes may have inconsistent light sources.',
        'difficulty': 'Hard'
    },
    {
        'title': 'Look for Temporal Glitches',
        'description': 'Watch frame-by-frame for sudden jumps in facial features, especially during head turns.',
        'difficulty': 'Hard'
    }
]


def get_signal_explanation(signal_type, score):
    """
    Get explanation for a signal score
    
    Args:
        signal_type: Type of signal ('vision', 'audio', 'temporal', 'quality')
        score: Signal score (0-1)
        
    Returns:
        Explanation dictionary
    """
    level = 'high' if score >= 0.5 else 'low'
    
    if signal_type in SIGNAL_EXPLANATIONS:
        return SIGNAL_EXPLANATIONS[signal_type][level]
    
    return {'title': 'Unknown Signal', 'explanation': 'No explanation available', 'indicators': []}


def generate_educational_content(analysis_result):
    """
    Generate educational content based on analysis
    
    Args:
        analysis_result: Complete analysis result
        
    Returns:
        Educational content dictionary
    """
    signals = analysis_result['signals']
    quality = analysis_result['quality_assessment']
    
    content = {
        'statistics': DEEPFAKE_STATS,
        'signal_explanations': {
            'vision': get_signal_explanation('vision', signals['vision']['score']),
            'audio': get_signal_explanation('audio', signals['audio']['score']),
            'temporal': get_signal_explanation('temporal', signals['temporal']['score']),
            'quality': get_signal_explanation('quality', quality['overall'])
        },
        'detection_tips': DETECTION_TIPS,
        'risk_assessment': generate_risk_assessment(analysis_result),
        'recommended_actions': generate_recommendations(analysis_result)
    }
    
    return content


def generate_risk_assessment(analysis_result):
    """
    Generate risk assessment based on detection result
    
    Args:
        analysis_result: Analysis result
        
    Returns:
        Risk assessment dictionary
    """
    score = analysis_result['trust_score']
    decision = analysis_result['decision']
    
    if score >= 0.7:
        risk_level = 'Low'
        risk_color = 'green'
        risk_description = 'Content appears authentic with strong validation signals.'
    elif score >= 0.4:
        risk_level = 'Medium'
        risk_color = 'orange'
        risk_description = 'Authenticity uncertain. Exercise caution and verify through other means.'
    else:
        risk_level = 'High'
        risk_color = 'red'
        risk_description = 'Strong indicators of manipulation. Do not trust without verification.'
    
    return {
        'level': risk_level,
        'color': risk_color,
        'description': risk_description,
        'confidence': abs(score - 0.5) * 2  # 0 to 1 scale
    }


def generate_recommendations(analysis_result):
    """
    Generate recommended actions based on result
    
    Args:
        analysis_result: Analysis result
        
    Returns:
        List of recommendations
    """
    score = analysis_result['trust_score']
    quality = analysis_result['quality_assessment']['overall']
    
    recommendations = []
    
    if quality < 0.5:
        recommendations.append({
            'icon': '⚠️',
            'title': 'Obtain Higher Quality Source',
            'description': 'The input quality limits analysis reliability. Try to find an original, uncompressed version.'
        })
    
    if score < 0.4:
        recommendations.append({
            'icon': '🚨',
            'title': 'Treat as Potentially Manipulated',
            'description': 'Multiple signals indicate manipulation. Do not share or trust this content.'
        })
        recommendations.append({
            'icon': '📢',
            'title': 'Report to Platforms',
            'description': 'If found on social media, report it to platform moderators for review.'
        })
    elif score < 0.7:
        recommendations.append({
            'icon': '🔍',
            'title': 'Verify Through Alternative Sources',
            'description': 'Cross-check with official sources, news outlets, or fact-checking organizations.'
        })
        recommendations.append({
            'icon': '👥',
            'title': 'Consult Experts',
            'description': 'For important decisions, consult digital forensics experts or fact-checkers.'
        })
    else:
        recommendations.append({
            'icon': '✅',
            'title': 'Content Appears Authentic',
            'description': 'Strong validation signals detected. However, always maintain healthy skepticism.'
        })
        recommendations.append({
            'icon': '📌',
            'title': 'Save Verification Record',
            'description': 'Download the analysis report for future reference if needed.'
        })
    
    recommendations.append({
        'icon': '🎓',
        'title': 'Learn More About Deepfakes',
        'description': 'Stay informed about deepfake technology and detection methods.'
    })
    
    return recommendations
