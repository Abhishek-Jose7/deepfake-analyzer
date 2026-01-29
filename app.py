"""
Deepfake Trust System - Enhanced Flask Backend
Advanced multi-signal intelligence with comprehensive features
"""
from flask import Flask, request, jsonify, render_template, send_file
import os
import tempfile
import uuid
import cv2
import base64
from werkzeug.utils import secure_filename
from flask_cors import CORS

# Import signal extractors
from signals.vision import analyze_frames
from signals.audio import analyze_audio
from signals.temporal import analyze_temporal_signals

# Import trust engine
from trust_engine.scorer import trust_score, generate_report
from trust_engine.failure_modes import analyze_quality
from trust_engine.heatmap_generator import generate_composite_heatmap, frame_to_base64
from trust_engine.adversarial import apply_adversarial_attack, test_robustness
from trust_engine.report_generator import generate_html_report, save_html_report, generate_hash_fingerprint
from trust_engine.educational import generate_educational_content

# Import utilities
from utils.video_utils import extract_frames, get_video_metadata
from utils.audio_utils import extract_audio
from utils.batch_processor import batch_processor


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['REPORTS_FOLDER'] = os.path.join(tempfile.gettempdir(), 'deepfake_reports')

# Create reports folder
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """
    Main analysis endpoint
    
    Accepts video file and returns comprehensive trust analysis
    """
    try:
        # Check if file is present
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: mp4, avi, mov, mkv, webm'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Get video metadata
            metadata = get_video_metadata(filepath)
            
            # Extract frames (5 fps)
            frames = extract_frames(filepath, fps=5)
            
            if not frames:
                return jsonify({'error': 'Could not extract frames from video'}), 400
            
            # Extract audio
            audio_path = extract_audio(filepath)
            
            # Analyze signals
            print("Analyzing vision signals...")
            vision_score = analyze_frames(frames)
            
            print("Analyzing audio signals...")
            audio_data = analyze_audio(audio_path)
            audio_score = audio_data['combined']
            
            print("Analyzing temporal signals...")
            temporal_data = analyze_temporal_signals(frames)
            temporal_score = temporal_data['combined']
            
            print("Analyzing quality...")
            quality_data = analyze_quality(frames)
            quality_score = quality_data['overall']
            
            # Calculate trust score
            final_score, decision, reason = trust_score(
                vision_score, 
                audio_score, 
                temporal_score, 
                quality_score
            )
            
            # Generate comprehensive report
            report = generate_report(
                {'combined': vision_score, 'artifact_score': vision_score, 'edge_consistency': vision_score},
                audio_data,
                temporal_data,
                quality_data,
                final_score,
                decision,
                reason
            )
            
            # Add metadata
            report['metadata'] = {
                'filename': filename,
                'duration': round(metadata['duration'], 2),
                'fps': round(metadata['fps'], 2),
                'resolution': f"{metadata['width']}x{metadata['height']}",
                'frames_analyzed': len(frames)
            }
            
            # Cleanup
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            os.remove(filepath)
            
            return jsonify(report)
            
        except Exception as e:
            # Cleanup on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system': 'Deepfake Trust System',
        'version': '2.0.0',
        'features': [
            'multi-signal-analysis',
            'heatmap-visualization',
            'adversarial-robustness',
            'batch-processing',
            'html-reports',
            'educational-content',
            'blockchain-verification'
        ]
    })


@app.route('/api/analyze/heatmap', methods=['POST'])
def analyze_with_heatmap():
    """
    Enhanced analysis endpoint that includes heatmap visualization
    
    Returns analysis result with heatmap overlays showing suspicious regions
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            frames = extract_frames(filepath, fps=5)
            if not frames:
                return jsonify({'error': 'Could not extract frames'}), 400
            
            # Generate heatmaps for sample frames
            sample_indices = [0, len(frames)//2, len(frames)-1] if len(frames) >= 3 else [0]
            heatmaps = []
            
            for idx in sample_indices:
                if idx < len(frames):
                    heatmap_data = generate_composite_heatmap(frames[idx], frames, idx)
                    
                    # Convert to base64 for JSON response
                    heatmaps.append({
                        'frame_index': idx,
                        'artifact_heatmap': frame_to_base64(heatmap_data['artifact']['overlay']),
                        'edge_heatmap': frame_to_base64(heatmap_data['edge']['overlay']),
                        'temporal_heatmap': frame_to_base64(heatmap_data['temporal']['overlay']) if 'temporal' in heatmap_data else None
                    })
            
            # Clean up
            os.remove(filepath)
            
            return jsonify({
                'heatmaps': heatmaps,
                'total_frames': len(frames),
                'message': 'Heatmaps generated successfully'
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Heatmap generation failed: {str(e)}'}), 500


@app.route('/api/analyze/adversarial', methods=['POST'])
def adversarial_test():
    """
    Test detection robustness under adversarial attacks
    
    Applies various degradations and shows how detection holds up
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            frames = extract_frames(filepath, fps=5)
            audio_path = extract_audio(filepath)
            
            # Define simple analyze function for robustness testing
            def analyze_frames_simple(test_frames):
                v_score = analyze_frames(test_frames)
                return v_score
            
            # Test robustness
            robustness_results = test_robustness(frames, analyze_frames_simple)
            
            # Clean up
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            os.remove(filepath)
            
            return jsonify({
                'robustness_test': robustness_results,
                'message': 'Adversarial testing complete',
                'interpretation': {
                    'original_score': robustness_results['original'],
                    'most_resilient_to': min(robustness_results['attacks'].items(), key=lambda x: x[1]['degradation'])[0] if robustness_results['attacks'] else None,
                    'most_vulnerable_to': max(robustness_results['attacks'].items(), key=lambda x: x[1]['degradation'])[0] if robustness_results['attacks'] else None
                }
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Adversarial testing failed: {str(e)}'}), 500


@app.route('/api/analyze/educational', methods=['POST'])
def analyze_with_education():
    """
    Full analysis with educational explanations
    
    Includes signal explanations, detection tips, and recommendations
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        # Run standard analysis first
        result = analyze_video()
        
        if isinstance(result, tuple):  # Error response
            return result
        
        # Get the JSON data
        analysis_result = result.get_json()
        
        # Generate educational content
        educational_content = generate_educational_content(analysis_result)
        
        # Combine results
        enhanced_result = {
            **analysis_result,
            'educational_content': educational_content
        }
        
        return jsonify(enhanced_result)
        
    except Exception as e:
        return jsonify({'error': f'Educational analysis failed: {str(e)}'}), 500


@app.route('/api/report/generate', methods=['POST'])
def generate_report_endpoint():
    """
    Generate downloadable HTML report
    
    Creates a comprehensive report with verification hash
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Get metadata
            metadata = get_video_metadata(filepath)
            
            # Extract and analyze
            frames = extract_frames(filepath, fps=5)
            audio_path = extract_audio(filepath)
            
            # Analyze signals
            vision_score = analyze_frames(frames)
            audio_data = analyze_audio(audio_path)
            temporal_data = analyze_temporal_signals(frames)
            quality_data = analyze_quality(frames)
            
            # Calculate trust score
            final_score, decision, reason = trust_score(
                vision_score,
                audio_data['combined'],
                temporal_data['combined'],
                quality_data['overall']
            )
            
            # Generate report
            report = generate_report(
                {'combined': vision_score, 'artifact_score': vision_score, 'edge_consistency': vision_score},
                audio_data,
                temporal_data,
                quality_data,
                final_score,
                decision,
                reason
            )
            
            report['metadata'] = {
                'filename': filename,
                'duration': round(metadata['duration'], 2),
                'fps': round(metadata['fps'], 2),
                'resolution': f"{metadata['width']}x{metadata['height']}",
                'frames_analyzed': len(frames)
            }
            
            # Generate HTML report
            html_content = generate_html_report(report, filepath)
            
            # Save report
            report_id = str(uuid.uuid4())
            report_filename = f"deepfake_report_{report_id}.html"
            report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
            save_html_report(html_content, report_path)
            
            # Get verification hash
            video_hash = generate_hash_fingerprint(filepath)
            
            # Clean up
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            os.remove(filepath)
            
            return jsonify({
                'report_id': report_id,
                'report_url': f'/api/report/download/{report_id}',
                'verification_hash': video_hash,
                'message': 'Report generated successfully'
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


@app.route('/api/report/download/<report_id>', methods=['GET'])
def download_report(report_id):
    """
    Download generated HTML report
    """
    try:
        report_filename = f"deepfake_report_{report_id}.html"
        report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report not found'}), 404
        
        return send_file(report_path, as_attachment=True, download_name=f'deepfake_analysis_{report_id}.html')
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/api/batch/create', methods=['POST'])
def create_batch_job():
    """
    Create a batch processing job for multiple videos
    """
    try:
        # This would handle multiple file uploads
        # For now, return the structure
        job_id = str(uuid.uuid4())
        
        files = request.files.getlist('videos')
        if not files:
            return jsonify({'error': 'No videos provided'}), 400
        
        # Save files temporarily
        file_paths = []
        for file in files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
                file.save(filepath)
                file_paths.append(filepath)
        
        if not file_paths:
            return jsonify({'error': 'No valid video files'}), 400
        
        # Create batch job
        job = batch_processor.create_job(job_id, file_paths)
        
        return jsonify({
            'job_id': job_id,
            'status': job['status'],
            'total_files': job['total'],
            'status_url': f'/api/batch/status/{job_id}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Batch creation failed: {str(e)}'}), 500


@app.route('/api/batch/status/<job_id>', methods=['GET'])
def get_batch_status(job_id):
    """
    Get status of a batch processing job
    """
    try:
        status = batch_processor.get_job_status(job_id)
        
        if status is None:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': f'Status fetch failed: {str(e)}'}), 500


@app.route('/api/compare', methods=['POST'])
def compare_videos():
    """
    Compare two videos side-by-side
    
    Useful for comparing original vs suspected deepfake
    """
    try:
        if 'video1' not in request.files or 'video2' not in request.files:
            return jsonify({'error': 'Two videos required for comparison'}), 400
        
        file1 = request.files['video1']
        file2 = request.files['video2']
        
        # Analyze both videos
        results = {}
        
        for idx, file in enumerate([file1, file2], 1):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                frames = extract_frames(filepath, fps=5)
                audio_path = extract_audio(filepath)
                
                vision_score = analyze_frames(frames)
                audio_data = analyze_audio(audio_path)
                temporal_data = analyze_temporal_signals(frames)
                quality_data = analyze_quality(frames)
                
                final_score, decision, reason = trust_score(
                    vision_score,
                    audio_data['combined'],
                    temporal_data['combined'],
                    quality_data['overall']
                )
                
                results[f'video{idx}'] = {
                    'filename': filename,
                    'trust_score': final_score,
                    'decision': decision,
                    'signals': {
                        'vision': vision_score,
                        'audio': audio_data['combined'],
                        'temporal': temporal_data['combined'],
                        'quality': quality_data['overall']
                    }
                }
                
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)
                os.remove(filepath)
                
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                results[f'video{idx}'] = {'error': str(e)}
        
        # Calculate difference
        if 'error' not in results['video1'] and 'error' not in results['video2']:
            results['comparison'] = {
                'trust_score_diff': abs(results['video1']['trust_score'] - results['video2']['trust_score']),
                'vision_diff': abs(results['video1']['signals']['vision'] - results['video2']['signals']['vision']),
                'audio_diff': abs(results['video1']['signals']['audio'] - results['video2']['signals']['audio']),
                'temporal_diff': abs(results['video1']['signals']['temporal'] - results['video2']['signals']['temporal']),
                'verdict': 'Significantly Different' if abs(results['video1']['trust_score'] - results['video2']['trust_score']) > 0.3 else 'Similar'
            }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Comparison failed: {str(e)}'}), 500


@app.route('/api/verify/hash', methods=['POST'])
def verify_hash():
    """
    Verify video using blockchain-style hash
    """
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        video_hash = generate_hash_fingerprint(filepath)
        
        os.remove(filepath)
        
        return jsonify({
            'filename': filename,
            'sha256_hash': video_hash,
            'verification_timestamp': str(uuid.uuid4()),
            'message': 'Hash generated for blockchain verification'
        })
        
    except Exception as e:
        return jsonify({'error': f'Hash verification failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

