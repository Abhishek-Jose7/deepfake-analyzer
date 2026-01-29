# 🛠️ Troubleshooting v2.0

If you encounter issues with the new Frontend setup, here are the fixes we just applied.

## 1. "Website looks broken / Only plain text"
**Cause**: Tailwind CSS v4 requires different configuration than v3.
**Fix Applied**: Updated `globals.css` to use `@import "tailwindcss";` instead of `@tailwind` directives.

## 2. "ImportError: cannot import name 'frame_to_base64'"
**Cause**: The backend was missing a helper function in `heatmap_generator.py`.
**Fix Applied**: Added the missing function to `c:\deepfak\trust_engine\heatmap_generator.py`.

---

## 🔄 How to Restart

To ensure all fixes apply, please:

1. **Stop** both terminal processes (Ctrl+C).
2. **Restart Backend**:
   ```powershell
   cd c:\deepfak
   python app.py
   ```
3. **Restart Frontend**:
   ```powershell
   cd c:\deepfak\frontend
   npm run dev
   ```

## 🧹 Cache Clearing (If styling still looks off)
If the website still looks unstyled, delete the `.next` folder and restart:
```powershell
cd c:\deepfak\frontend
rm -r .next
npm run dev
```

Everything should now work perfectly! 🚀
