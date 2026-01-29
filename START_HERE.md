# 🎯 GETTING STARTED - FULL STACK

Welcome to the Deepfake Trust System! This guide will get you up and running with the new Web Interface.

---

## ⚡ Quick Start (Double Terminal Setup)

You need **two terminal windows** running simultaneously.

### Terminal 1: The Brain (Backend)
Runs the Python AI engine.

```powershell
cd c:\deepfak
python app.py
```
*Expected Output: "Running on http://127.0.0.1:5000"*

### Terminal 2: The Face (Frontend)
Runs the modern Next.js interface.

```powershell
cd c:\deepfak\frontend
npm run dev
```
*Expected Output: "Ready in ... http://localhost:3000"*

---

## 🚀 Access the System

Open your browser and navigate to:
👉 **http://localhost:3000**

(Do not go to localhost:5000 anymore - that's just the API engine working in the background)

---

## 📋 What You Can Do Now

### 1. 🔍 Deep Analysis
- Upload a video to get a Trust Score
- **New**: Select "Heatmap Mode" to see visual artifacts!
- **New**: Select "Robustness Mode" to test against attacks.

### 2. ⚡ Batch Processing
- Click "Batch" in the nav
- Select 3+ videos at once
- Watch them process in parallel

### 3. 🔄 Comparison
- Click "Compare" in the nav
- Upload an Original vs Fake video
- See side-by-side signal differences

### 4. 📄 Professional Reports
- Generate a PDF-ready HTML report
- Includes a **Blockchain Verification Hash**

---

## 🛠️ Troubleshooting

**"Connection Error" / "Analysis Failed"**
- Is the Backend (Terminal 1) running?
- Is it on port 5000?

**"Upload stuck"**
- Check the Backend terminal for error messages.
- Max file size is 100MB.

---

## 🏗️ Architecture

- **Frontend**: Next.js 14, TypeScript, TailwindCSS, Framer Motion
- **Backend**: Flask, OpenCV, NumPy, Librosa
- **Communication**: REST API (with CORS enabled)

---

**Good luck with the competition! 🚀**
