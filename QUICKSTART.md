# 🚀 Quick Start Guide

Get the Deepfake Trust System running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ FFmpeg installed (see below if not)

### Quick FFmpeg Check
```bash
ffmpeg -version
```

If this fails, install FFmpeg first (see SETUP.md).

## Installation Steps

### 1. Navigate to Project
```bash
cd c:\deepfak
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- OpenCV (video processing)
- librosa (audio analysis)
- numpy (numerical computing)

**Note**: Installation takes 2-5 minutes.

### 3. Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### 4. Open in Browser
Navigate to: **http://localhost:5000**

## First Test

### Test Video Requirements
- **Format**: MP4, AVI, MOV, MKV, or WEBM
- **Size**: Under 100MB
- **Duration**: 5-30 seconds recommended
- **Content**: Video with people speaking (best results)

### Where to Get Test Videos

**Free Stock Videos**:
1. Visit https://pexels.com/videos/
2. Search "person talking" or "interview"
3. Download a short clip

**Your Own Content**:
- Record a 10-second selfie video on your phone
- Transfer to computer
- Upload to the system

### Running Your First Analysis

1. Click **"Choose Video File"**
2. Select your test video
3. Click **"Analyze Video"**
4. Wait 15-30 seconds
5. View results!

## Understanding Results

### Trust Score
- **0.7 - 1.0**: Real (high confidence)
- **0.5 - 0.7**: Likely Real
- **0.3 - 0.5**: Ambiguous
- **0.0 - 0.3**: Likely Fake / Fake

### Key Signals to Watch

**Vision Score**: 
- Checks for visual artifacts
- Over-smoothed skin = lower score

**Audio Score**:
- Analyzes voice characteristics
- Synthetic voices score lower

**Temporal Score**:
- THE SECRET WEAPON
- Checks frame-to-frame consistency
- Deepfakes struggle here

**Quality Assessment**:
- Critical for trust calibration
- Low quality → System reduces confidence
- **This is what makes it smart!**

## Quick Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### "FFmpeg not found"
Install FFmpeg (see SETUP.md) or:
```bash
# Windows (with Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### "Port already in use"
Edit `app.py`, change line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### "Analysis takes too long"
- Use shorter videos (10-20 seconds)
- Lower resolution videos process faster
- First run is always slower

## Next Steps

### Test Different Scenarios

1. **Real Video** → Should get high trust score
2. **Screen Recording of Video** → Quality assessment triggers
3. **Compressed Video** → System should be ambiguous

### Explore the Code

Start with:
- `app.py` - Main application
- `trust_engine/scorer.py` - Decision logic
- `signals/temporal.py` - The secret weapon

### Customize

Try adjusting weights in `trust_engine/scorer.py`:
```python
weights = {
    "vision": 0.4,    # Change these
    "audio": 0.3,     # to experiment
    "temporal": 0.3   # with different
}                     # configurations
```

## API Testing

### Using cURL
```bash
curl -X POST -F "video=@test_video.mp4" http://localhost:5000/api/analyze
```

### Using Python
```python
import requests

files = {'video': open('video.mp4', 'rb')}
response = requests.post('http://localhost:5000/api/analyze', files=files)
print(response.json())
```

## The Key Line

When demonstrating this system, remember to say:

> **"Our system degrades confidence instead of hallucinating certainty."**

This is what makes it trustworthy.

## Files Overview

```
deepfak/
├── app.py              ← Start here (Flask backend)
├── requirements.txt    ← Dependencies
├── README.md          ← Full documentation
├── SETUP.md           ← Detailed setup
├── ARCHITECTURE.md    ← Technical deep dive
│
├── signals/           ← Signal extractors
│   ├── vision.py      ← Visual artifact detection
│   ├── audio.py       ← Audio analysis
│   └── temporal.py    ← Frame consistency (secret weapon)
│
├── trust_engine/      ← Decision logic
│   ├── scorer.py      ← Trust score calculation
│   └── failure_modes.py ← Quality assessment
│
├── utils/             ← Helpers
│   ├── video_utils.py
│   └── audio_utils.py
│
├── static/            ← Frontend
│   ├── style.css      ← Styling
│   └── script.js      ← Interactions
│
└── templates/         ← HTML
    └── index.html     ← Main UI
```

## Success Checklist

- [ ] Python installed
- [ ] FFmpeg installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs (`python app.py`)
- [ ] Browser shows UI (http://localhost:5000)
- [ ] Test video analyzed successfully
- [ ] Results displayed with scores

## Need Help?

Check the detailed guides:
- **Installation issues**: See `SETUP.md`
- **Understanding the system**: See `ARCHITECTURE.md`
- **Full documentation**: See `README.md`

---

**You're ready to detect deepfakes! 🎯**

Remember: This system combines **weak signals** with **strong logic** to create something smarter than the sum of its parts.
