---
title: DeepTrust API
emoji: 🛡️
colorFrom: gray
colorTo: indigo
sdk: docker
app_port: 7860
---

# DeepTrust API

Multi-signal deepfake detection with explainable AI.

## API Endpoints

- `POST /api/analyze` - Standard video analysis
- `POST /api/analyze/heatmap` - Analysis with visual heatmaps
- `POST /api/analyze/adversarial` - Adversarial robustness testing
- `POST /api/analyze/educational` - Educational analysis mode
- `POST /api/batch/create` - Create batch processing job
- `GET /api/batch/status/{job_id}` - Get batch job status
- `POST /api/compare` - Compare two videos
- `POST /api/report/generate` - Generate evidence report
- `GET /api/report/download/{report_id}` - Download report
- `POST /api/verify/hash` - Get video verification hash

## Usage

```bash
curl -X POST https://your-space.hf.space/api/analyze \
  -F "video=@your_video.mp4"
```
