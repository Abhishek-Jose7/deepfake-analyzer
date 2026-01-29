# Deepfake Trust System - Setup Guide

## Quick Start

### 1. Install FFmpeg

FFmpeg is required for audio extraction from videos.

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Verify: Open Command Prompt and type `ffmpeg -version`

**Alternative for Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Verify FFmpeg installation:**
```bash
ffmpeg -version
```

### 2. Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd c:\deepfak

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Testing the System

### Demo Video Creation

You can test with any video file, but here are some sources:

1. **Real Videos**: Use your phone camera or download from:
   - Pexels (https://www.pexels.com/videos/)
   - Pixabay (https://pixabay.com/videos/)

2. **Deepfake Videos**: For testing purposes:
   - Search YouTube for "deepfake detection dataset"
   - FaceForensics++ dataset (academic access)

### Expected Behavior

**Real Video (High Quality)**:
- Trust Score: 0.7 - 0.9
- Decision: "Real" or "Likely Real"
- All signals > 0.6

**Deepfake Video**:
- Trust Score: 0.2 - 0.4
- Decision: "Fake" or "Likely Fake"
- Temporal signal usually < 0.4

**Compressed/Low Quality**:
- Trust Score: Variable with reduced confidence
- Decision: "Ambiguous"
- Quality assessment < 0.5

## Troubleshooting

### FFmpeg Not Found
```
Error: ffmpeg not found
```
**Solution**: Install FFmpeg and add to PATH

### librosa Installation Issues
```
Error: Failed building wheel for librosa
```
**Solution (Windows)**:
```bash
pip install --upgrade pip setuptools wheel
pip install librosa --no-cache-dir
```

### OpenCV Issues
```
Error: cv2 module not found
```
**Solution**:
```bash
pip install opencv-python --upgrade
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## API Testing

### Using cURL

```bash
curl -X POST -F "video=@test_video.mp4" http://localhost:5000/api/analyze
```

### Using Python

```python
import requests

url = 'http://localhost:5000/api/analyze'
files = {'video': open('test_video.mp4', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### Using Postman

1. Method: POST
2. URL: `http://localhost:5000/api/analyze`
3. Body: form-data
4. Key: `video`, Type: File
5. Select your video file

## Performance Tips

### For Faster Analysis
- Use shorter videos (10-30 seconds)
- Lower resolution videos process faster
- The system samples frames (not all frames analyzed)

### For Production
- Set `debug=False` in `app.py`
- Use a production WSGI server (gunicorn, waitress)
- Add request queuing for concurrent uploads

## Next Steps

1. **Test with different videos**: Try real, fake, compressed
2. **Analyze the signals**: Understand which signals trigger for which videos
3. **Customize thresholds**: Adjust weights in `trust_engine/scorer.py`
4. **Extend functionality**: Add new signal extractors

## Key Demonstration Points

When presenting this system:

1. **Show quality awareness**: Same video, different compressions
2. **Explain signals**: What each signal detects
3. **Highlight calibration**: How confidence reduces on poor quality
4. **Compare outputs**: Real vs Fake side-by-side

Remember the key message:

> **"Our system degrades confidence instead of hallucinating certainty."**

This makes the system trustworthy and defensible.
