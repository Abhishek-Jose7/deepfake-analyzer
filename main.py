"""
DeepTrust API - FastAPI Backend with LLM Integration
Enhanced with Llama 3.2 Vision via Groq API
Deployable on Hugging Face Spaces
"""

import os
import uuid
import shutil
import hashlib
import base64
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from contextlib import asynccontextmanager

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

# Import enhanced analyzers
from signals.enhanced_vision import analyze_vision
from signals.audio_signal import analyze_audio
from signals.temporal_signal import analyze_temporal
from model.inference import analyze_frames as analyze_frames_dl  # Deep Learning Model
from trust_engine.score_fusion import calculate_trust_score, generate_report
from trust_engine.heatmap_generator import generate_composite_heatmap, frame_to_base64
from trust_engine.adversarial import test_robustness
from trust_engine.educational import generate_educational_content
from trust_engine.report_generator import generate_html_report
from utils.video_processing import extract_frames, extract_audio
from utils.batch_processor import BatchProcessor

# Import LLM analyzer
try:
    from llm.groq_analyzer import groq_analyzer
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    groq_analyzer = None

# Configuration
UPLOAD_DIR = Path("uploads")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Batch processor instance
batch_processor = BatchProcessor(max_workers=3)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 DeepTrust API starting...")
    if LLM_AVAILABLE and groq_analyzer and groq_analyzer.enabled:
        print("✅ Groq LLM integration enabled (Llama 3.2 Vision)")
    else:
        print("⚠️ LLM integration disabled - set GROQ_API_KEY for enhanced analysis")
    yield
    print("👋 DeepTrust API shutting down...")
    # Cleanup
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    UPLOAD_DIR.mkdir(exist_ok=True)


# Create FastAPI app
app = FastAPI(
    title="DeepTrust API",
    description="Multi-signal deepfake detection with Llama 3.2 Vision AI & EfficientNet",
    version="2.2.0",
    lifespan=lifespan
)

# CORS - Allow all origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Models ==============

class AnalysisResult(BaseModel):
    trust_score: float
    decision: str
    confidence: str
    reason: str
    signals: dict
    model_prediction: Optional[dict] = None  # Deep Learning Model Result
    llm_analysis: Optional[dict] = None
    quality_assessment: Optional[dict] = None


class BatchJobStatus(BaseModel):
    job_id: str
    status: str
    total: int
    completed: int
    progress: float
    results: List[dict]


# ============== Helper Functions ==============

def save_upload_file(upload_file: UploadFile) -> Path:
    """Save uploaded file and return path"""
    file_id = str(uuid.uuid4())
    file_ext = Path(upload_file.filename).suffix or ".mp4"
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path


def cleanup_file(file_path: Path):
    """Remove temporary file"""
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception:
        pass


def run_analysis(video_path: Path, include_llm: bool = True) -> dict:
    """
    Core analysis pipeline with DL Model + Signal Analysis + LLM
    
    Args:
        video_path: Path to video file
        include_llm: Whether to include LLM analysis
        
    Returns:
        Complete analysis results
    """
    frames = extract_frames(str(video_path), max_frames=30)
    audio_path = extract_audio(str(video_path))
    
    if len(frames) == 0:
        return {
            "trust_score": 0.5,
            "decision": "Analysis Failed",
            "confidence": "none",
            "reason": "Could not extract frames from video",
            "signals": {},
            "model_prediction": None,
            "llm_analysis": None
        }
    
    # 1. Deep Learning Model Analysis (EfficientNet)
    dl_result = analyze_frames_dl(frames)
    
    # 2. Enhanced Signal Analysis
    vision_result = analyze_vision(frames)
    audio_result = analyze_audio(audio_path) if audio_path else {"score": 0.5, "confidence": 0.0}
    temporal_result = analyze_temporal(frames)
    
    signals = {
        "vision": vision_result,
        "audio": audio_result,
        "temporal": temporal_result
    }
    
    # 3. Calculate Base Trust Score (Signal Fusion)
    trust_score, quality_assessment = calculate_trust_score(signals)
    
    # 4. Integrate Deep Learning Model Score
    # We weight the DL model heavily if it's confident
    if dl_result["success"]:
        dl_score = dl_result["score"]  # Probability of being REAL
        dl_conf = dl_result["confidence"]
        
        # Weighted fusion: 40% Signals, 60% DL Model (if model loaded)
        if dl_result.get("model_loaded", False):
            trust_score = (trust_score * 0.4) + (dl_score * 0.6)
        else:
            # If model not loaded/pretrained only, trust signals more
            trust_score = (trust_score * 0.7) + (dl_score * 0.3)
    
    # Generate basic report
    report = generate_report(trust_score, signals, quality_assessment)
    
    # 5. LLM Analysis (Llama 3.2 Vision)
    llm_analysis = None
    if include_llm and LLM_AVAILABLE and groq_analyzer and groq_analyzer.enabled:
        signal_scores = {
            "vision": vision_result.get("score", 0.5),
            "audio": audio_result.get("score", 0.5),
            "temporal": temporal_result.get("score", 0.5),
            "model_probability": dl_result.get("score", 0.5) if dl_result["success"] else 0.5
        }
        llm_analysis = groq_analyzer.analyze_frames(frames, signal_scores)
        
        # Adjust trust score based on LLM analysis if it has high confidence
        if llm_analysis and llm_analysis.get("parsed"):
            parsed = llm_analysis["parsed"]
            llm_confidence = parsed.get("confidence", "medium")
            llm_verdict = parsed.get("verdict", "uncertain")
            
            # If LLM has high confidence, use it to refine the score
            if llm_confidence == "high":
                if llm_verdict == "authentic":
                    # Boost towards 1.0, but respect existing evidence
                    trust_score = (trust_score * 0.7) + 0.3
                elif llm_verdict == "manipulated":
                    # Pull towards 0.0
                    trust_score = (trust_score * 0.7)
            
            # Update reason with LLM insight
            if parsed.get("reasoning"):
                report["reason"] = parsed["reasoning"]
    
    # Cleanup audio
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)
    
    # Final Decision Logic
    if trust_score >= 0.8:
        decision = "Likely Real"
    elif trust_score >= 0.6:
        decision = "Possibly Real"
    elif trust_score >= 0.4:
        decision = "Ambiguous"
    elif trust_score >= 0.2:
        decision = "Possibly Fake"
    else:
        decision = "Likely Fake"
    
    return {
        "trust_score": trust_score,
        "decision": decision,
        "confidence": report["confidence"],
        "reason": report["reason"],
        "signals": signals,
        "model_prediction": dl_result,
        "llm_analysis": llm_analysis,
        "quality_assessment": quality_assessment
    }


# ============== Routes ==============

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "DeepTrust API",
        "version": "2.1.0",
        "llm_enabled": LLM_AVAILABLE and groq_analyzer and groq_analyzer.enabled,
        "llm_model": "llama-3.2-90b-vision-preview" if (LLM_AVAILABLE and groq_analyzer and groq_analyzer.enabled) else None,
        "endpoints": {
            "analyze": "/api/analyze",
            "heatmap": "/api/analyze/heatmap",
            "adversarial": "/api/analyze/adversarial",
            "educational": "/api/analyze/educational",
            "batch_create": "/api/batch/create",
            "batch_status": "/api/batch/status/{job_id}",
            "compare": "/api/compare",
            "report_generate": "/api/report/generate",
            "report_download": "/api/report/download/{report_id}",
            "verify_hash": "/api/verify/hash"
        }
    }


@app.post("/api/analyze")
async def analyze_video(
    video: UploadFile = File(...), 
    background_tasks: BackgroundTasks = None,
    use_llm: bool = True
):
    """
    Standard analysis for video or image with optional LLM enhancement
    
    Args:
        video: Video or image file to analyze
        use_llm: Whether to use LLM for enhanced analysis (default: True)
    """
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    video_path = save_upload_file(video)
    
    try:
        result = run_analysis(video_path, include_llm=use_llm)
        return JSONResponse(content=result)
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, video_path)
        else:
            cleanup_file(video_path)


@app.post("/api/analyze/heatmap")
async def analyze_with_heatmap(video: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Analysis with visual heatmaps"""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    video_path = save_upload_file(video)
    
    try:
        frames = extract_frames(str(video_path), max_frames=30)
        
        if len(frames) == 0:
            raise HTTPException(status_code=400, detail="Could not extract frames")
        
        # Run standard analysis with LLM
        result = run_analysis(video_path, include_llm=True)
        
        # Generate heatmaps for sample frames
        heatmaps = []
        sample_indices = [0, len(frames)//2, len(frames)-1] if len(frames) >= 3 else range(len(frames))
        
        for idx in sample_indices:
            if idx < len(frames):
                heatmap_data = generate_composite_heatmap(frames[idx], frames, idx)
                heatmaps.append({
                    "frame_index": idx,
                    "artifact_heatmap": frame_to_base64(heatmap_data["artifact"]["overlay"]),
                    "edge_heatmap": frame_to_base64(heatmap_data["edge"]["overlay"])
                })
        
        result["heatmaps"] = heatmaps
        return JSONResponse(content=result)
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, video_path)
        else:
            cleanup_file(video_path)


@app.post("/api/analyze/adversarial")
async def analyze_adversarial(video: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Adversarial robustness testing"""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    video_path = save_upload_file(video)
    
    try:
        frames = extract_frames(str(video_path), max_frames=30)
        
        if len(frames) == 0:
            raise HTTPException(status_code=400, detail="Could not extract frames")
        
        # Run standard analysis
        result = run_analysis(video_path, include_llm=True)
        
        # Run robustness testing
        def analyze_function(test_frames):
            vision_result = analyze_vision(test_frames)
            return vision_result.get("score", 0.5)
        
        robustness = test_robustness(frames, analyze_function)
        result["robustness_test"] = robustness
        
        return JSONResponse(content=result)
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, video_path)
        else:
            cleanup_file(video_path)


@app.post("/api/analyze/educational")
async def analyze_educational(video: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Educational analysis with explanations"""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    video_path = save_upload_file(video)
    
    try:
        result = run_analysis(video_path, include_llm=True)
        
        # Add educational content
        educational = generate_educational_content(result)
        result["educational"] = educational
        
        # Generate LLM explanation if available
        if LLM_AVAILABLE and groq_analyzer and groq_analyzer.enabled:
            explanation = groq_analyzer.generate_explanation(result)
            result["llm_explanation"] = explanation
        
        return JSONResponse(content=result)
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, video_path)
        else:
            cleanup_file(video_path)


@app.post("/api/batch/create")
async def create_batch_job(videos: List[UploadFile] = File(...)):
    """Create a batch processing job"""
    if not videos:
        raise HTTPException(status_code=400, detail="No video files provided")
    
    job_id = str(uuid.uuid4())
    file_paths = []
    
    for video in videos:
        if video.filename:
            path = save_upload_file(video)
            file_paths.append({"path": str(path), "filename": video.filename})
    
    if not file_paths:
        raise HTTPException(status_code=400, detail="No valid video files")
    
    # Create job
    batch_processor.create_job(job_id, file_paths)
    
    # Start processing in background (without LLM for speed)
    def process_job():
        def analyze_func(video_path):
            return run_analysis(Path(video_path), include_llm=False)
        batch_processor.start_processing(job_id, analyze_func)
    
    import threading
    thread = threading.Thread(target=process_job)
    thread.start()
    
    return JSONResponse(content={
        "job_id": job_id,
        "total_files": len(file_paths),
        "status": "pending"
    })


@app.get("/api/batch/status/{job_id}")
async def get_batch_status(job_id: str):
    """Get batch job status"""
    status = batch_processor.get_job_status(job_id)
    
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JSONResponse(content=status)


@app.post("/api/compare")
async def compare_videos(
    video1: UploadFile = File(...),
    video2: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Compare two videos"""
    if not video1.filename or not video2.filename:
        raise HTTPException(status_code=400, detail="Two video files required")
    
    path1 = save_upload_file(video1)
    path2 = save_upload_file(video2)
    
    try:
        result1 = run_analysis(path1, include_llm=True)
        result2 = run_analysis(path2, include_llm=True)
        
        # Calculate comparison
        score_diff = abs(result1["trust_score"] - result2["trust_score"])
        verdict = "Similar" if score_diff < 0.15 else "Different"
        
        return JSONResponse(content={
            "video1": {
                "filename": video1.filename,
                **result1
            },
            "video2": {
                "filename": video2.filename,
                **result2
            },
            "comparison": {
                "trust_score_diff": score_diff,
                "verdict": verdict
            }
        })
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, path1)
            background_tasks.add_task(cleanup_file, path2)
        else:
            cleanup_file(path1)
            cleanup_file(path2)


@app.post("/api/report/generate")
async def generate_report_endpoint(video: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Generate HTML evidence report"""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    video_path = save_upload_file(video)
    
    try:
        result = run_analysis(video_path, include_llm=True)
        
        # Generate report
        report_id = str(uuid.uuid4())
        report_path = REPORTS_DIR / f"{report_id}.html"
        
        frames = extract_frames(str(video_path), max_frames=5)
        html_content = generate_html_report(result, str(video_path), frames)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Generate verification hash
        with open(report_path, "rb") as f:
            verification_hash = hashlib.sha256(f.read()).hexdigest()
        
        return JSONResponse(content={
            "report_id": report_id,
            "report_url": f"/api/report/download/{report_id}",
            "verification_hash": verification_hash,
            "analysis": result
        })
    finally:
        if background_tasks:
            background_tasks.add_task(cleanup_file, video_path)
        else:
            cleanup_file(video_path)


@app.get("/api/report/download/{report_id}")
async def download_report(report_id: str):
    """Download generated report"""
    report_path = REPORTS_DIR / f"{report_id}.html"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=str(report_path),
        filename=f"deeptrust_report_{report_id}.html",
        media_type="text/html"
    )


@app.post("/api/verify/hash")
async def verify_hash(video: UploadFile = File(...)):
    """Get video verification hash"""
    if not video.filename:
        raise HTTPException(status_code=400, detail="No video file provided")
    
    # Calculate hash from content
    content = await video.read()
    video_hash = hashlib.sha256(content).hexdigest()
    
    return JSONResponse(content={
        "filename": video.filename,
        "sha256": video_hash,
        "timestamp": datetime.now().isoformat()
    })


# ============== Run Server ==============

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face uses 7860
    uvicorn.run(app, host="0.0.0.0", port=port)
