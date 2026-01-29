// DOM Elements
const videoInput = document.getElementById('videoInput');
const uploadBtn = document.getElementById('uploadBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

const uploadSection = document.getElementById('uploadSection');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');

const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

let selectedFile = null;

// Upload button click
uploadBtn.addEventListener('click', () => {
    videoInput.click();
});

// File selection
videoInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        selectedFile = file;
        fileName.textContent = file.name;
        fileInfo.style.display = 'flex';
    }
});

// Analyze button click
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Show progress section
    uploadSection.style.display = 'none';
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Simulate progress states
    updateProgress(20, 'Extracting frames from video...');
    
    // Prepare form data
    const formData = new FormData();
    formData.append('video', selectedFile);
    
    try {
        updateProgress(40, 'Analyzing vision signals...');
        
        // Make API request
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        updateProgress(60, 'Analyzing audio signals...');
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        updateProgress(80, 'Calculating trust score...');
        
        const result = await response.json();
        
        updateProgress(100, 'Analysis complete!');
        
        // Wait a moment before showing results
        setTimeout(() => {
            displayResults(result);
        }, 500);
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Analysis failed: ${error.message}`);
        resetToUpload();
    }
});

// New analysis button
newAnalysisBtn.addEventListener('click', () => {
    resetToUpload();
});

// Update progress
function updateProgress(percent, text) {
    progressFill.style.width = `${percent}%`;
    progressText.textContent = text;
}

// Display results
function displayResults(data) {
    progressSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Set verdict
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictText = document.getElementById('verdictText');
    const trustScoreValue = document.getElementById('trustScoreValue');
    const verdictReason = document.getElementById('verdictReason');
    
    verdictText.textContent = data.decision;
    trustScoreValue.textContent = data.trust_score.toFixed(2);
    verdictReason.textContent = data.reason;
    
    // Set verdict icon class and emoji
    verdictIcon.className = 'verdict-icon';
    if (data.decision === 'Real' || data.decision === 'Likely Real') {
        verdictIcon.classList.add('real');
        verdictIcon.textContent = '✓';
    } else if (data.decision === 'Fake' || data.decision === 'Likely Fake') {
        verdictIcon.classList.add('fake');
        verdictIcon.textContent = '✗';
    } else {
        verdictIcon.classList.add('ambiguous');
        verdictIcon.textContent = '?';
    }
    
    // Set signal bars
    setSignalBar('vision', data.signals.vision.score);
    setSignalBar('audio', data.signals.audio.score);
    setSignalBar('temporal', data.signals.temporal.score);
    setSignalBar('quality', data.quality_assessment.overall);
    
    // Set vision details
    document.getElementById('artifactScore').textContent = data.signals.vision.artifact_detection.toFixed(2);
    document.getElementById('edgeScore').textContent = data.signals.vision.edge_consistency.toFixed(2);
    
    // Set audio details
    document.getElementById('flatnessScore').textContent = data.signals.audio.spectral_flatness.toFixed(2);
    document.getElementById('rolloffScore').textContent = data.signals.audio.spectral_rolloff.toFixed(2);
    
    // Set temporal details
    document.getElementById('consistencyScore').textContent = data.signals.temporal.consistency.toFixed(2);
    document.getElementById('varianceScore').textContent = data.signals.temporal.variance.toFixed(2);
    
    // Set quality details
    document.getElementById('compressionScore').textContent = data.quality_assessment.compression.toFixed(2);
    document.getElementById('resolutionScore').textContent = data.quality_assessment.resolution.toFixed(2);
    
    // Set metadata
    document.getElementById('metaFilename').textContent = data.metadata.filename;
    document.getElementById('metaDuration').textContent = `${data.metadata.duration}s`;
    document.getElementById('metaResolution').textContent = data.metadata.resolution;
    document.getElementById('metaFrames').textContent = data.metadata.frames_analyzed;
    
    // Animate signal bars
    setTimeout(() => {
        document.querySelectorAll('.signal-fill').forEach(fill => {
            const width = fill.dataset.width;
            fill.style.width = `${width * 100}%`;
        });
    }, 100);
}

// Set signal bar
function setSignalBar(type, value) {
    const fill = document.getElementById(`${type}Fill`);
    const valueSpan = document.getElementById(`${type}Value`);
    
    fill.dataset.width = value;
    fill.style.width = '0%'; // Start at 0 for animation
    valueSpan.textContent = value.toFixed(2);
}

// Reset to upload state
function resetToUpload() {
    uploadSection.style.display = 'block';
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    
    fileInfo.style.display = 'none';
    fileName.textContent = '';
    selectedFile = null;
    videoInput.value = '';
    
    progressFill.style.width = '0%';
    progressText.textContent = '';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Deepfake Trust System initialized');
});
