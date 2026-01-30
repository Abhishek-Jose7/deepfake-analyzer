import kagglehub
import shutil
import os
from pathlib import Path

def setup_cifake():
    print("⬇️ Downloading CIFAKE dataset (Images)...")
    path = kagglehub.dataset_download("birdy654/cifake-real-and-ai-generated-synthetic-images")
    print(f"✅ Downloaded to cache: {path}")
    
    # Target directory
    target_dir = Path("dataset")
    if target_dir.exists():
        print(f"⚠️ 'dataset' folder already exists. Skipping overwrite to avoid data loss.")
        print(f"You can use the downloaded data from: {path}")
        return

    target_dir.mkdir(parents=True)
    
    source_path = Path(path)
    
    # Check structure
    print("📂 Organizing files...")
    
    # Move/Copy Train
    if (source_path / "train").exists():
        shutil.copytree(source_path / "train", target_dir / "train")
        print("  - Copied train set")
        
    # Move/Copy Test -> Val
    if (source_path / "test").exists():
        shutil.copytree(source_path / "test", target_dir / "val")
        print("  - Copied test set to 'val'")
        
    print("\n✅ Dataset setup complete!")
    print(f"Location: {target_dir.absolute()}")
    print("\n🚀 To train:")
    print("python train.py --dataset dataset --dataset-type generic")

def setup_faceforensics():
    print("⬇️ Downloading FaceForensics++ (Video)...")
    path = kagglehub.dataset_download("hungle3401/faceforensics")
    print(f"✅ Downloaded to cache: {path}")
    
    target_dir = Path("dataset_ff")
    if target_dir.exists():
        print(f"⚠️ 'dataset_ff' folder already exists.")
    else:
        # Just copy the whole thing or symlink
        try:
            shutil.copytree(path, target_dir)
            print("✅ Copied to dataset_ff")
        except Exception as e:
            print(f"⚠️ Could not copy files: {e}")
            print(f"Data is at: {path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cifake", action="store_true", help="Download CIFAKE (Images)")
    parser.add_argument("--ff", action="store_true", help="Download FaceForensics (Video)")
    
    args = parser.parse_args()
    
    if args.cifake:
        setup_cifake()
    elif args.ff:
        setup_faceforensics()
    else:
        print("Please specify --cifake or --ff")
