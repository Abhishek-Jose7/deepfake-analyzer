# DeepTrust Model Training Guide

This guide explains how to train your own custom EfficientNet-based deepfake detection model using the included training script.

---

## 1. Prepare Your Dataset

You need a dataset of real and fake videos or frames. The system supports a generic folder structure or the FaceForensics++ structure.

### Generic Structure (Recommended)
This is the easiest way to organize your data:

```
dataset/
├── train/
│   ├── real/
│   │   ├── video1.mp4
│   │   └── img1.jpg
│   └── fake/
│       ├── video2.mp4
│       └── img2.jpg
├── val/
│   ├── real/
│   └── fake/
└── test/ (optional)
    ├── real/
    └── fake/
```

- You can mix video files (.mp4, .avi) and image files (.jpg, .png).
- The system automatically extracts frames from videos.
- `train` is for training, `val` for validation during training, `test` for final evaluation.

---

## 2. Start Training

Run the `train.py` script. The default settings use `efficientnet_b0` which is a good balance of speed and accuracy.

```bash
# Basic training
python train.py --dataset path/to/dataset --epochs 50

# Using a larger model (EfficientNet B3)
python train.py --dataset path/to/dataset --backbone efficientnet_b3 --batch-size 8

# Using FaceForensics++ structure
python train.py --dataset path/to/ff_data --dataset-type faceforensics
```

### Key Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--dataset` | Path to dataset folder | (Required) |
| `--epochs` | Number of training epochs | 50 |
| `--batch-size` | Batch size (reduce if OOM) | 16 |
| `--backbone` | Model architecture (efficientnet_b0..b7) | efficientnet_b0 |
| `--lr` | Learning rate | 0.0001 |
| `--frames-per-video`| Frames to sample per video file | 16 |
| `--patience` | Early stopping patience | 10 |

---

## 3. Training Process

The script performs the following:

1. **Data Loading**: 
   - Extract frames from videos
   - Detect and crop faces (focus on facial regions)
   - Apply augmentations (rotation, color jitter, flip)

2. **Model Training**:
   - Uses **EfficientNet** as the backbone
   - Applies **Self-Attention** to focus on manipulation artifacts
   - Optimizes using **AdamW** with cosine learning rate schedule
   - Uses **Mixed Precision (AMP)** for speed on GPUs

3. **Validation**:
   - Evaluates on validation set after every epoch
   - Saves best model based on accuracy

4. **Output**:
   - Saves checkpoints to `checkpoints/` folder
   - `best.pth`: The model with highest validation accuracy
   - `latest.pth`: The most recent checkpoint
   - `history.json`: Training metrics log

---

## 4. Using the Trained Model

Once trained, the API automatically picks up the model if placed correctly.

1. **Locate your model**: It will be in `checkpoints/best.pth`
2. **Move it** (Optional): You can move it to `model/pretrained/best.pth`
3. **Restart the API**:
   ```bash
   python main.py
   ```
   The API will log: `✅ Model loaded from checkpoints/best.pth`

4. **Verify**:
   Analyze a video on the frontend. The `Trust Score` will now be heavily influenced (60%) by your trained model's prediction.

---

## 5. Troubleshooting

**Out of Memory (OOM) Error:**
- Reduce `--batch-size` (e.g., to 8 or 4)
- Reduce `--frames-per-video` (e.g., to 8)
- Use a smaller backbone (`efficientnet_b0`)

**Low Accuracy:**
- Ensure your dataset is balanced (equal real/fake)
- Increase `--epochs`
- try a larger backbone (`efficientnet_b4`)
- Check if face detection operates correctly on your data

**"timm not available":**
- Install requirements: `pip install timm`
