"""
Report Generator - PDF Export with Evidence
Generates comprehensive PDF reports for analysis results
"""
import os
import cv2
import base64
from io import BytesIO
from datetime import datetime
import hashlib


def generate_hash_fingerprint(video_path):
    """
    Generate SHA-256 hash fingerprint for verification
    
    Args:
        video_path: Path to video file
        
    Returns:
        Hash string
    """
    sha256 = hashlib.sha256()
    
    with open(video_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    
    return sha256.hexdigest()


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


def generate_html_report(analysis_result, video_path, sample_frames=None, heatmaps=None):
    """
    Generate HTML report with all analysis details
    
    Args:
        analysis_result: Complete analysis result dictionary
        video_path: Path to analyzed video
        sample_frames: Sample frames from video (optional)
        heatmaps: Generated heatmaps (optional)
        
    Returns:
        HTML report string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    video_hash = generate_hash_fingerprint(video_path) if os.path.exists(video_path) else "N/A"
    
    # Convert decision to color
    decision = analysis_result['decision']
    if 'Real' in decision:
        verdict_color = '#43e97b'
        verdict_icon = '✓'
    elif 'Fake' in decision:
        verdict_color = '#fa709a'
        verdict_icon = '✗'
    else:
        verdict_color = '#ffa500'
        verdict_icon = '?'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Deepfake Analysis Report</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                padding: 40px 20px;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
            }}
            .header p {{
                opacity: 0.9;
            }}
            .section {{
                padding: 30px 40px;
                border-bottom: 1px solid #e0e0e0;
            }}
            .section:last-child {{
                border-bottom: none;
            }}
            .section h2 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 1.5rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .verdict {{
                text-align: center;
                padding: 40px;
                background: #f9f9f9;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .verdict-icon {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: {verdict_color};
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                margin: 0 auto 20px;
            }}
            .verdict h3 {{
                font-size: 2rem;
                color: {verdict_color};
                margin-bottom: 10px;
            }}
            .trust-score {{
                font-size: 3rem;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 20px 0;
            }}
            .info-item {{
                background: #f9f9f9;
                padding: 15px;
                border-radius: 6px;
            }}
            .info-label {{
                font-size: 0.85rem;
                color: #666;
                margin-bottom: 5px;
            }}
            .info-value {{
                font-size: 1.1rem;
                font-weight: 600;
                color: #333;
            }}
            .signal-bar {{
                margin: 15px 0;
            }}
            .signal-name {{
                font-weight: 600;
                margin-bottom: 5px;
                color: #333;
            }}
            .bar-container {{
                background: #e0e0e0;
                height: 30px;
                border-radius: 15px;
                overflow: hidden;
                position: relative;
            }}
            .bar-fill {{
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding-right: 10px;
                color: white;
                font-weight: 600;
                transition: width 0.5s ease;
            }}
            .hash {{
                font-family: monospace;
                background: #f0f0f0;
                padding: 10px;
                border-radius: 4px;
                word-break: break-all;
                font-size: 0.9rem;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background: #f9f9f9;
                color: #666;
                font-size: 0.9rem;
            }}
            .frame-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin: 20px 0;
            }}
            .frame-item img {{
                width: 100%;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Deepfake Analysis Report</h1>
                <p>Comprehensive Multi-Signal Intelligence Analysis</p>
            </div>
            
            <div class="section">
                <div class="verdict">
                    <div class="verdict-icon">{verdict_icon}</div>
                    <h3>{decision}</h3>
                    <div class="trust-score">{analysis_result['trust_score']:.2f}</div>
                    <p style="color: #666; margin-top: 10px;">{analysis_result['reason']}</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Signal Analysis</h2>
                
                <div class="signal-bar">
                    <div class="signal-name">Vision Signal</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {analysis_result['signals']['vision']['score']*100}%">
                            {analysis_result['signals']['vision']['score']:.2f}
                        </div>
                    </div>
                </div>
                
                <div class="signal-bar">
                    <div class="signal-name">Audio Signal</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {analysis_result['signals']['audio']['score']*100}%; background: linear-gradient(90deg, #f093fb, #f5576c)">
                            {analysis_result['signals']['audio']['score']:.2f}
                        </div>
                    </div>
                </div>
                
                <div class="signal-bar">
                    <div class="signal-name">Temporal Signal</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {analysis_result['signals']['temporal']['score']*100}%; background: linear-gradient(90deg, #4facfe, #00f2fe)">
                            {analysis_result['signals']['temporal']['score']:.2f}
                        </div>
                    </div>
                </div>
                
                <div class="signal-bar">
                    <div class="signal-name">Quality Assessment</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {analysis_result['quality_assessment']['overall']*100}%; background: linear-gradient(90deg, #43e97b, #38f9d7)">
                            {analysis_result['quality_assessment']['overall']:.2f}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📹 Video Metadata</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Filename</div>
                        <div class="info-value">{analysis_result['metadata']['filename']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Duration</div>
                        <div class="info-value">{analysis_result['metadata']['duration']}s</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Resolution</div>
                        <div class="info-value">{analysis_result['metadata']['resolution']}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Frames Analyzed</div>
                        <div class="info-value">{analysis_result['metadata']['frames_analyzed']}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔐 Verification Hash</h2>
                <p style="margin-bottom: 10px; color: #666;">SHA-256 fingerprint for blockchain verification:</p>
                <div class="hash">{video_hash}</div>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #999;">
                    Analysis timestamp: {timestamp}
                </p>
            </div>
            
            <div class="footer">
                <p>Generated by <strong>Deepfake Trust System</strong></p>
                <p>"Our system degrades confidence instead of hallucinating certainty."</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def save_html_report(html_content, output_path):
    """
    Save HTML report to file
    
    Args:
        html_content: HTML string
        output_path: Output file path
        
    Returns:
        Path to saved report
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path
