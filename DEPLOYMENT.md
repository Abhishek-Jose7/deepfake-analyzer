# DeepTrust Deployment Guide

This guide covers deploying the DeepTrust system with:
- **Backend** → Hugging Face Spaces (Docker)
- **Frontend** → Vercel

---

## 1. Backend Deployment (Hugging Face Spaces)

### Prerequisites
- Hugging Face account
- Git installed

### Steps

1. **Create a new Space on Hugging Face**
   - Go to https://huggingface.co/new-space
   - Space name: `deeptrust-api`
   - Select **Docker** as the SDK
   - Choose **CPU basic** (free tier)
   - Visibility: Public or Private

2. **Clone the Space and push your code**
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

   # Push to Hugging Face
   git add .
   git commit -m "Initial deployment"
   git push
   ```

3. **Your API will be available at:**
   ```
   https://YOUR_USERNAME-deeptrust-api.hf.space
   ```

### File Structure for Hugging Face
```
deeptrust-api/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── README.md              # Space description (with YAML frontmatter)
├── signals/               # Signal analysis modules
│   ├── __init__.py
│   ├── vision.py
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
└── utils/                 # Utility modules
    ├── __init__.py
    ├── video_processing.py
    └── batch_processor.py
```

---

## 2. Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier works)
- GitHub account

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
python main.py
# API runs at http://localhost:7860
```

### Start Frontend
```bash
cd c:\deepfak\frontend
npm run dev
# Frontend runs at http://localhost:3000
```

### Environment Variables (Local)
Create `.env.local` in the frontend folder:
```
NEXT_PUBLIC_API_URL=http://localhost:7860
```

---

## 4. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/analyze` | POST | Standard analysis |
| `/api/analyze/heatmap` | POST | Analysis with heatmaps |
| `/api/analyze/adversarial` | POST | Robustness testing |
| `/api/analyze/educational` | POST | Educational mode |
| `/api/batch/create` | POST | Create batch job |
| `/api/batch/status/{id}` | GET | Batch status |
| `/api/compare` | POST | Compare two videos |
| `/api/report/generate` | POST | Generate report |
| `/api/report/download/{id}` | GET | Download report |
| `/api/verify/hash` | POST | Get verification hash |

---

## 5. Testing the API

```bash
# Health check
curl https://YOUR_USERNAME-deeptrust-api.hf.space/

# Upload and analyze a video
curl -X POST \
  https://YOUR_USERNAME-deeptrust-api.hf.space/api/analyze \
  -F "video=@your_video.mp4"
```

---

## 6. Troubleshooting

### CORS Issues
The backend allows all origins by default. If you face CORS issues:
1. Check browser console for specific error
2. Verify the API URL is correct in Vercel environment variables
3. Make sure the API is responding (test with curl)

### Deployment Fails
- **Hugging Face**: Check build logs in the Space settings
- **Vercel**: Check the deployment logs in the Vercel dashboard

### API Not Responding
- Hugging Faces Spaces may sleep after inactivity
- First request after sleep may take 30-60 seconds
