# 🎨 Frontend Architecture Summary

## Stack Overview
The Deepfake Trust System now features a premium, production-grade frontend built with:
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS + PostCSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Design System**: Glassmorphism (Dark Mode)

## 📱 Pages & Features

### 1. **Landing Page (`/`)**
- Hero section with gradient typography
- Animated feature grid
- Live stats dashboard
- "Core Principle" highlight section

### 2. **Analysis Dashboard (`/analyze`)**
- **Dynamic Mode Switcher**:
  - `Standard`: Trust score + Signal breakdown
  - `Heatmap`: Visual artifact overlays (Base64 decoded)
  - `Adversarial`: Robustness metrics table
  - `Educational`: Risk assessment + tips
- **Real-time States**: Loading spinners, error handling, drag-and-drop

### 3. **Batch Processor (`/batch`)**
- Multi-file upload interface
- Real-time polling of backend job status
- Progress bar visualization
- Per-file result cards

### 4. **Comparison Tool (`/compare`)**
- Dual upload slots (Original vs Suspect)
- Side-by-side metric table
- Differential highlighting (Green/Red indicators)

### 5. **Evidence Reports (`/reports`)**
- Report generation wizard
- Blockchain hash display
- Direct HTML report download

### 6. **Documentation (`/docs`)**
- Philosophy guide
- Signal pipeline visualization
- API reference cheat sheet

## 🔧 Technical Implementation Details

### **Responsive Design**
- Mobile-first approach
- Hamburger menu for mobile navigation
- Grid layouts that adapt (1 col -> 2 col -> 3 col)

### **State Management**
- React `useState` for local UI state
- `useEffect` + `setInterval` for polling batch jobs
- `framer-motion` for page transitions and entry animations

### **Backend Integration**
- Environment variable `NEXT_PUBLIC_API_URL` configuration
- `FormData` handling for file uploads
- Error boundary handling for API failures

## 🎨 Design Philosophy
- **"Trust through Transparency"**: The UI relies on glassmorphism to convey depth and transparency.
- **"Premium AI"**: Gradients (Cyan -> Purple) create a modern, high-tech aesthetic.
- **"Actionable Intelligence"**: Results are color-coded (Green/Yellow/Red) for instant decision making.

---

**Status**: 🚀 **Production Ready**
