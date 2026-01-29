# DeepTrust Deployment Guide

This guide covers deploying the DeepTrust system with:
- **Backend** → Hugging Face Spaces (Docker) with Llama 3.2 Vision AI
- **Frontend** → Vercel

---

## 🔑 Prerequisites: Get Your Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up / Log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

This key enables **Llama 3.2 Vision** for intelligent deepfake analysis!

---

## 1. Backend Deployment (Hugging Face Spaces)

### Steps

1. **Create a new Space on Hugging Face**
   - Go to https://huggingface.co/new-space
   - Space name: `deeptrust-api`
   - Select **Docker** as the SDK
   - Choose **CPU basic** (free tier)
   - Visibility: Public or Private

2. **Add the Groq API Key as a Secret**
   - Go to your Space → Settings → Secrets
   - Add a new secret:
     - Name: `GROQ_API_KEY`
     - Value: Your Groq API key (gsk_...)

3. **Clone the Space and push your code**
   ```bash
   # Clone your new Space
   git clone https://huggingface.co/spaces/YOUR_USERNAME/deeptrust-api
   cd deeptrust-api

   # Copy backend files (from c:\deepfak)
   # - main.py
   # - requirements.txt
   # - Dockerfile
   # - README.md
   # - signals/ folder
   # - trust_engine/ folder
   # - utils/ folder
   # - llm/ folder (NEW - for Groq integration)

   # Push to Hugging Face
   git add .
   git commit -m "Deploy with Llama 3.2 Vision"
   git push
   ```

4. **Your API will be available at:**
   ```
   https://YOUR_USERNAME-deeptrust-api.hf.space
   ```

### File Structure for Hugging Face
```
deeptrust-api/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── README.md              # Space description
├── signals/               # Signal analysis modules
│   ├── __init__.py
│   ├── vision.py
│   ├── enhanced_vision.py  # NEW - 7 detection techniques
│   ├── vision_signal.py
│   ├── audio.py
│   ├── audio_signal.py
│   ├── temporal.py
│   └── temporal_signal.py
├── trust_engine/          # Trust score engine
│   ├── __init__.py
│   ├── score_fusion.py
│   ├── heatmap_generator.py
│   ├── adversarial.py
│   ├── educational.py
│   └── report_generator.py
├── llm/                   # NEW - LLM integration
│   ├── __init__.py
│   └── groq_analyzer.py   # Llama 3.2 Vision integration
└── utils/
    ├── __init__.py
    ├── video_processing.py
    └── batch_processor.py
```

---

## 2. Frontend Deployment (Vercel)

### Steps

1. **Push frontend to GitHub**
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "Initial frontend"
   git remote add origin https://github.com/YOUR_USERNAME/deeptrust-frontend.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Framework preset: **Next.js**

3. **Set Environment Variables in Vercel**
   - Go to Project Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL = https://YOUR_USERNAME-deeptrust-api.hf.space
     ```

4. **Deploy**
   - Click "Deploy"
   - Your frontend will be at: `https://your-project.vercel.app`

---

## 3. Local Development

### Start Backend
```bash
cd c:\deepfak

# Set Groq API key (Windows PowerShell)
$env:GROQ_API_KEY = "gsk_your_key_here"

# Or create .env file with:
# GROQ_API_KEY=gsk_your_key_here

python main.py
# API runs at http://localhost:7860
```

### Start Frontend
```bash
cd c:\deepfak\frontend
npm run dev
# Frontend runs at http://localhost:3000
```

---

## 4. How the Analysis Works

### Signal Analysis (7 Detection Techniques)

1. **Laplacian Variance** - Detects blur/smoothing
2. **Edge Consistency** - Analyzes edge sharpness and density
3. **Color Distribution** - Checks for unnatural color uniformity
4. **Noise Analysis** - Detects over-processing
5. **Face Analysis** - Examines face regions for manipulation artifacts
6. **Compression Artifacts** - Detects double compression
7. **Frequency Domain** - Analyzes FFT for GAN artifacts

### LLM Analysis (Llama 3.2 Vision)

When the Groq API key is configured, the system also:
- Sends video frames to Llama 3.2 Vision
- Gets intelligent visual analysis
- Combines signal scores with LLM reasoning
- Provides natural language explanations

---

## 5. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check (shows LLM status) |
| `/api/analyze` | POST | Standard analysis with LLM |
| `/api/analyze/heatmap` | POST | Analysis with visual heatmaps |
| `/api/analyze/adversarial` | POST | Robustness testing |
| `/api/analyze/educational` | POST | Educational mode with explanations |
| `/api/batch/create` | POST | Create batch job |
| `/api/batch/status/{id}` | GET | Batch status |
| `/api/compare` | POST | Compare two videos |
| `/api/report/generate` | POST | Generate evidence report |
| `/api/report/download/{id}` | GET | Download report |
| `/api/verify/hash` | POST | Get verification hash |

---

## 6. Testing the API

```bash
# Health check (shows LLM status)
curl https://YOUR_USERNAME-deeptrust-api.hf.space/

# Expected response:
{
  "status": "online",
  "service": "DeepTrust API",
  "version": "2.1.0",
  "llm_enabled": true,
  "llm_model": "llama-3.2-90b-vision-preview",
  "endpoints": {...}
}

# Upload and analyze a video
curl -X POST \
  https://YOUR_USERNAME-deeptrust-api.hf.space/api/analyze \
  -F "video=@your_video.mp4"
```

---

## 7. Troubleshooting

### LLM Not Working
- Check if `GROQ_API_KEY` is set correctly as a Space Secret
- Verify the key is valid at https://console.groq.com/
- Check Space logs for errors

### Analysis Too Slow
- First request may take 30-60 seconds (Space waking up)
- LLM analysis adds 5-10 seconds
- Use `use_llm=false` query param for faster analysis without LLM

### CORS Issues
- The backend allows all origins by default
- Check browser console for specific errors
- Verify the API URL in Vercel environment variables

### Hugging Face Space Errors
- Check build logs in Space settings
- Ensure all files are committed (especially `llm/` folder)
- Verify Dockerfile syntax
