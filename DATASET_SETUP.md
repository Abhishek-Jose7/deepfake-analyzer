# Deepfake Datasets Guide

To train your model effectively, you need a good dataset. Here are the best options for 2024/2025.

---

## 🚀 Option 1: The "Quick Start" (Images)
**Dataset:** **CIFAKE** (Real vs AI Generated)  
**Best for:** Detecting AI-generated images (Midjourney, Stable Diffusion).  
**Size:** ~60,000 images.  
**Download:** [Search "CIFAKE Kaggle"](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images)

### How to use it:
1. Download and unzip.
2. Organize it like this:
   ```
   dataset/
   ├── train/
   │   ├── real/  (Put 'REAL' images here)
   │   └── fake/  (Put 'FAKE' images here)
   ├── val/       (Rename 'test' to 'val' if needed)
       ├── real/
       └── fake/
   ```
   *Note: The script expects a `val` folder for validation. If you only have `train` and `test`, rename `test` to `val` or copy some training data there.*
3. **Train Command:**
   ```bash
   python train.py --dataset dataset --dataset-type generic
   ```

---

## 🎥 Option 2: The "Gold Standard" (Video)
**Dataset:** **FaceForensics++**  
**Best for:** Detecting Face Swaps and Reenactment videos.  
**Size:** ~1000 original videos + 4000 manipulated versions.  
**Download:** [GitHub Page](https://github.com/ondyari/FaceForensics) (Requires filling a form).

### How to use it:
1. Download the "c23" (high quality) or "c40" (low quality) version.
2. Keep the original structure (`original_sequences`, `manipulated_sequences`).
3. **Train Command:**
   ```bash
   python train.py --dataset path/to/faceforensics --dataset-type faceforensics
   ```

---

## 🔥 Option 3: High-Quality Video
**Dataset:** **Celeb-DF v2**  
**Best for:** Highly realistic deepfakes that are hard to spot.  
**Download:** [GitHub Page](https://github.com/yuezunli/celeb-deepfakeforensics)

### How to use it:
1. Extract frames or use the videos directly.
2. Structure it like Option 1 (Generic).
3. **Train Command:**
   ```bash
   python train.py --dataset dataset --dataset-type generic
   ```

---

## 🛠️ Custom Dataset (Your Own)
You can collect your own images/videos!

1. **Scrape Data**: Download real videos from YouTube, fake videos from social media.
2. **Structure**:
   ```
   dataset/
     train/
       real/
       fake/
   ```
3. **Run Training**:
   ```bash
   python train.py --dataset dataset --epochs 50
   ```
