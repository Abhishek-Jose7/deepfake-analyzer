# 🚀 Advanced API Documentation

## Deepfake Trust System v2.0 - Complete API Reference

---

## Overview

The enhanced Deepfake Trust System now includes **12+ powerful API endpoints** that make it a comprehensive, competition-winning platform. This goes far beyond basic deepfake detection.

---

## 🎯 Core Features

1. ✅ **Multi-Signal Analysis** - Vision, Audio, Temporal
2. ✅ **Heatmap Visualization** - Visual explanations
3. ✅ **Adversarial Robustness** - Test under attacks
4. ✅ **Batch Processing** - Multiple videos at once
5. ✅ **HTML Report Generation** - Professional reports
6. ✅ **Educational Dashboard** - Learn about deepfakes
7. ✅ **Comparison Mode** - Side-by-side analysis
8. ✅ **Blockchain Verification** - SHA-256 hashing

---

## 📡 API Endpoints

### 1. Basic Analysis

#### `POST /api/analyze`

**Standard deepfake analysis**

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/analyze
```

**Response**:
```json
{
  "trust_score": 0.85,
  "decision": "Real",
  "reason": "High Quality Input - Strong Real Signals",
  "signals": {
    "vision": {...},
    "audio": {...},
    "temporal": {...}
  },
  "quality_assessment": {...},
  "metadata": {...}
}
```

---

### 2. Heatmap Visualization 🔥 **NEW**

####`POST /api/analyze/heatmap`

**Generate visual heatmaps showing suspicious regions**

**What it does**: Creates artifact, edge, and temporal heatmaps that visually highlight suspicious areas in the video.

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/analyze/heatmap
```

**Response**:
```json
{
  "heatmaps": [
    {
      "frame_index": 0,
      "artifact_heatmap": "data:image/jpeg;base64,/9j/4AAQ...",
      "edge_heatmap": "data:image/jpeg;base64,/9j/4AAQ...",
      "temporal_heatmap": "data:image/jpeg;base64,/9j/4AAQ..."
    }
  ],
  "total_frames": 52,
  "message": "Heatmaps generated successfully"
}
```

**Use Case**: Show judges exactly WHERE the deepfake artifacts are

---

### 3. Adversarial Robustness Testing 🛡️ **NEW**

#### `POST /api/analyze/adversarial`

**Test detection under various attacks**

**What it does**: Applies compression, noise, blur, resolution changes, cropping, and color shifts to test robustness.

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/analyze/adversarial
```

**Response**:
```json
{
  "robustness_test": {
    "original": 0.78,
    "attacks": {
      "compression_low": {"score": 0.75, "degradation": 0.03},
      "compression_medium": {"score": 0.68, "degradation": 0.10},
      "compression_high": {"score": 0.52, "degradation": 0.26},
      "noise_medium": {"score": 0.71, "degradation": 0.07},
      "blur_medium": {"score": 0.69, "degradation": 0.09}
    }
  },
  "interpretation": {
    "most_resilient_to": "compression_low",
    "most_vulnerable_to": "compression_high"
  }
}
```

**Use Case**: Demonstrate robustness to WhatsApp/social media degradation

---

### 4. Educational Analysis 🎓 **NEW**

#### `POST /api/analyze/educational`

**Full analysis with educational explanations**

**What it does**: Same as standard analysis but adds statistics, detection tips, risk assessment, and recommendations.

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/analyze/educational
```

**Response**:
```json
{
  ...standard_analysis...,
  "educational_content": {
    "statistics": {
      "global_incidents": {...},
      "detection_accuracy": {...},
      "common_targets": [...]
    },
    "signal_explanations": {
      "vision": {
        "title": "Strong Visual Authenticity",
        "explanation": "...",
        "indicators": [...]
      }
    },
    "detection_tips": [...],
    "risk_assessment": {
      "level": "Low",
      "color": "green",
      "description": "...",
      "confidence": 0.92
    },
    "recommended_actions": [...]
  }
}
```

**Use Case**: Educate users about deepfakes while analyzing

---

### 5. Report Generation 📄 **NEW**

#### `POST /api/report/generate`

**Generate downloadable HTML report**

**What it does**: Creates professional HTML report with verification hash for evidence/legal use.

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/report/generate
```

**Response**:
```json
{
  "report_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "report_url": "/api/report/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "verification_hash": "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
  "message": "Report generated successfully"
}
```

#### `GET /api/report/download/<report_id>`

**Download the generated report**

**Request**:
```bash
curl http://localhost:5000/api/report/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890 -o report.html
```

**Use Case**: Generate evidence for fact-checkers, journalists, legal teams

---

### 6. Batch Processing ⚡ **NEW**

#### `POST /api/batch/create`

**Process multiple videos concurrently**

**Request**:
```bash
curl -X POST \
  -F "videos=@video1.mp4" \
  -F "videos=@video2.mp4" \
  -F "videos=@video3.mp4" \
  http://localhost:5000/api/batch/create
```

**Response**:
```json
{
  "job_id": "batch-12345678",
  "status": "pending",
  "total_files": 3,
  "status_url": "/api/batch/status/batch-12345678"
}
```

#### `GET /api/batch/status/<job_id>`

**Check batch job progress**

**Response**:
```json
{
  "id": "batch-12345678",
  "status": "processing",
  "total": 3,
  "completed": 2,
  "progress": 66.67,
  "results": [...],
  "errors": []
}
```

**Use Case**: Newsrooms processing multiple clips at once

---

### 7. Video Comparison 🔄 **NEW**

#### `POST /api/compare`

**Compare two videos side-by-side**

**What it does**: Analyzes two videos and shows differences in all signals.

**Request**:
```bash
curl -X POST \
  -F "video1=@original.mp4" \
  -F "video2=@suspected_fake.mp4" \
  http://localhost:5000/api/compare
```

**Response**:
```json
{
  "video1": {
    "filename": "original.mp4",
    "trust_score": 0.88,
    "decision": "Real",
    "signals": {...}
  },
  "video2": {
    "filename": "suspected_fake.mp4",
    "trust_score": 0.34,
    "decision": "Fake",
    "signals": {...}
  },
  "comparison": {
    "trust_score_diff": 0.54,
    "vision_diff": 0.42,
    "audio_diff": 0.38,
    "temporal_diff": 0.61,
    "verdict": "Significantly Different"
  }
}
```

**Use Case**: Compare original vs suspected manipulation

---

### 8. Blockchain Verification 🔐 **NEW**

#### `POST /api/verify/hash`

**Generate SHA-256 hash for blockchain verification**

**What it does**: Creates immutable fingerprint for video verification.

**Request**:
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/verify/hash
```

**Response**:
```json
{
  "filename": "video.mp4",
  "sha256_hash": "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
  "verification_timestamp": "uuid-timestamp",
  "message": "Hash generated for blockchain verification"
}
```

**Use Case**: Create verification trail for authentic content

---

### 9. Health Check

#### `GET /api/health`

**System status check**

**Response**:
```json
{
  "status": "healthy",
  "system": "Deepfake Trust System",
  "version": "2.0.0",
  "features": [
    "multi-signal-analysis",
    "heatmap-visualization",
    "adversarial-robustness",
    "batch-processing",
    "html-reports",
    "educational-content",
    "blockchain-verification"
  ]
}
```

---

## 🎯 Demonstration Scenarios

### Scenario 1: Basic Detection
```bash
curl -X POST -F "video=@real_video.mp4" http://localhost:5000/api/analyze
```
**Expected**: Trust score 0.7-0.9, "Real"

### Scenario 2: Visual Explanation
```bash
curl -X POST -F "video=@suspect_video.mp4" http://localhost:5000/api/analyze/heatmap
```
**Shows**: Heatmaps highlighting suspicious regions

### Scenario 3: Robustness Test
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/api/analyze/adversarial
```
**Demonstrates**: System handles degraded inputs gracefully

### Scenario 4: Professional Report
```bash
curl -X POST -F "video=@evidence.mp4" http://localhost:5000/api/report/generate
```
**Result**: Downloadable HTML report with verification hash

### Scenario 5: Batch Analysis
```bash
curl -X POST \
  -F "videos=@v1.mp4" \
  -F "videos=@v2.mp4" \
  -F "videos=@v3.mp4" \
  http://localhost:5000/api/batch/create
```
**Shows**: Processing multiple files concurrently

---

## 💡 Integration Examples

### Python Integration

```python
import requests

# Basic analysis
url = 'http://localhost:5000/api/analyze'  
files = {'video': open('video.mp4', 'rb')}
response = requests.post(url, files=files)
result = response.json()

print(f"Trust Score: {result['trust_score']}")
print(f"Decision: {result['decision']}")

# Get heatmaps
url = 'http://localhost:5000/api/analyze/heatmap'
response = requests.post(url, files=files)
heatmaps = response.json()['heatmaps']

# Save first heatmap
import base64
heatmap_data = heatmaps[0]['artifact_heatmap']
img_data = base64.b64decode(heatmap_data.split(',')[1])
with open('heatmap.jpg', 'wb') as f:
    f.write(img_data)
```

### JavaScript/Node.js Integration

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('video', fs.createReadStream('video.mp4'));

axios.post('http://localhost:5000/api/analyze', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Trust Score:', response.data.trust_score);
  console.log('Decision:', response.data.decision);
})
.catch(error => {
  console.error('Error:', error);
});
```

---

## 🏆 What Makes This Competition-Winning

### 1. **Beyond Basic Detection**
- Not just "fake or real"
- Shows WHERE and WHY
- Educational component

### 2. **Real-World Ready**
- Handles degraded inputs (adversarial testing)
- Batch processing for scale
- Professional reports for evidence

### 3. **Explainable AI**
- Heatmap visualization
- Signal-by-signal breakdown
- Human-readable explanations

### 4. **Production Features**
- RESTful API design
- Blockchain verification
- Comparison mode

### 5. **Honest Uncertainty**
- Quality-aware confidence
- Reduces trust on poor inputs
- Educational about limitations

---

## 📊 API Coverage Matrix

| Feature | Endpoint | Unique Value |
|---------|----------|--------------|
| Basic Detection | `/api/analyze` | Multi-signal intelligence |
| Visual Explanation | `/api/analyze/heatmap` | Shows suspicious regions |
| Robustness Test | `/api/analyze/adversarial` | Proves reliability |
| Education | `/api/analyze/educational` | User learning |
| Reports | `/api/report/generate` | Evidence generation |
| Batch Processing | `/api/batch/create` | Scalability |
| Comparison | `/api/compare` | Side-by-side analysis |
| Verification | `/api/verify/hash` | Blockchain-ready |

---

## 🎤 The Pitch

> "We've built a complete deepfake intelligence platform, not just a detector. Our system:
> 
> - **Explains visually** with heatmaps
> - **Proves robustness** under attacks
> - **Educates users** about deepfakes
> - **Generates evidence** with professional reports
> - **Scales to production** with batch processing
> - **Compares content** side-by-side
> - **Verifies authentically** with blockchain hashes
> 
> And most importantly: **It degrades confidence instead of hallucinating certainty.**"

---

**This is a system judges will remember. 🚀**
