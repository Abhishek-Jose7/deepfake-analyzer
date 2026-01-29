# System Architecture & Signal Analysis

## Overview

The Deepfake Trust System is built on the principle of **intelligent signal combination** rather than deep learning models. This approach is faster to implement, more explainable, and gracefully handles edge cases.

## Architecture Layers

### Layer 1: Signal Extractors

Each signal extractor is independent and focuses on a specific modality.

#### 1. Vision Signal (`signals/vision.py`)

**Purpose**: Detect visual artifacts in individual frames

**Techniques**:
- **Laplacian Variance**: Measures texture detail
  - Real videos: High variance (500-2000)
  - Deepfakes: Lower variance due to over-smoothing
  - Formula: `variance = Laplacian(frame).var()`

- **Edge Consistency**: Analyzes edge patterns
  - Uses Canny edge detection
  - Measures edge density
  - Normal range: 0.1 - 0.3

**Why it works**: Deepfake generators often over-smooth to hide artifacts, reducing high-frequency details.

#### 2. Audio Signal (`signals/audio.py`)

**Purpose**: Detect synthetic audio characteristics

**Techniques**:
- **Spectral Flatness**: Measures "noisiness" vs "tonality"
  - Natural speech: 0.05 - 0.2
  - Synthetic (TTS): 0.3 - 0.7
  - Formula: `geometric_mean / arithmetic_mean` of power spectrum

- **Spectral Rolloff**: Energy distribution across frequencies
  - Real speech typically: ~85% of Nyquist frequency
  - Synthetic may deviate significantly

- **Zero Crossing Rate**: Sign changes in waveform
  - Natural speech: 0.05 - 0.15
  - Indicates presence of unvoiced sounds

**Why it works**: TTS systems have different spectral characteristics than natural human voice production.

#### 3. Temporal Signal (`signals/temporal.py`)

**Purpose**: Detect inconsistencies across time - THE SECRET WEAPON

**Techniques**:
- **Temporal Consistency**: Frame-to-frame differences
  - Measures `mean(abs_diff(frame_t, frame_t+1))`
  - Real videos: Smooth, consistent changes
  - Deepfakes: Erratic, unstable changes

- **Temporal Variance**: Stability of frame differences
  - Low variance = stable = trustworthy
  - High variance = erratic = suspicious

- **Optical Flow**: Motion field analysis
  - Uses Farneback algorithm
  - Detects inconsistent motion patterns
  - Deepfakes often have flow discontinuities

**Why it works**: Deepfake generators process frames independently or with limited temporal context, creating temporal artifacts invisible in single frames.

### Layer 2: Quality Assessment (`trust_engine/failure_modes.py`)

**Purpose**: Assess input quality to calibrate confidence

**Critical Insight**: Poor quality input = Low confidence, regardless of signals

**Metrics**:
- **Compression Level**: Edge density analysis
  - Heavy compression destroys analysis reliability
  - Detection: Edge density < 0.1

- **Blocking Artifacts**: JPEG/H.264 block boundaries
  - Gradient variance indicates blocking
  - Reduces signal reliability

- **Noise Level**: Signal-to-noise estimation
  - Median filtering difference
  - High noise masks deepfake artifacts

- **Resolution Quality**: Pixel count assessment
  - Minimum: 640x480
  - Optimal: 1280x720+
  - Low resolution limits detection

**Why it's critical**: This prevents false accusations on degraded videos. The system says "I don't know" instead of guessing.

### Layer 3: Trust Scoring Engine (`trust_engine/scorer.py`)

**Purpose**: Intelligently combine signals with quality-aware calibration

**Algorithm**:

```python
# Base weighted combination
raw_score = 0.4 * vision + 0.3 * audio + 0.3 * temporal

# Quality-based adjustment
if quality < 0.3:
    final_score = raw_score * 0.4
    decision = "Ambiguous - Very Low Quality"
elif quality < 0.5:
    final_score = raw_score * 0.6
    decision = "Ambiguous - Low Quality"
elif quality < 0.7:
    final_score = raw_score * 0.85
    # Thresholds: 0.65, 0.35
else:
    final_score = raw_score
    # Thresholds: 0.7, 0.3
```

**Decision Thresholds** (for high quality):
- **Real**: Score > 0.7
- **Likely Real**: Score > 0.55
- **Ambiguous**: 0.45 ≤ Score ≤ 0.55
- **Likely Fake**: Score < 0.45
- **Fake**: Score < 0.3

**Explanation Generation**:
- Identifies which signals are weak
- Adds specific insights to reason
- Examples:
  - "high temporal inconsistency"
  - "visual artifacts detected"
  - "synthetic audio characteristics"

## Signal Weights Rationale

### Why Vision = 0.4?
- Most immediately visible to humans
- Strong indicator when present
- But can be fooled by compression

### Why Audio = 0.3?
- Very effective on TTS deepfakes
- Less susceptible to compression
- May not be present in all videos

### Why Temporal = 0.3?
- The "secret weapon"
- Hardest for deepfakes to fake
- Requires processing full video
- Can be noisy with camera movement

## Edge Cases Handling

### Case 1: Static Video (No Motion)
- Temporal signal may be unreliable
- System relies more on vision and audio
- Quality assessment detects static content

### Case 2: No Audio
- Audio signal returns 0.5 (neutral)
- System adapts weights internally
- Decision based on vision + temporal

### Case 3: Heavy Compression
- Quality score < 0.3
- Confidence multiplier: 0.4
- Forces "Ambiguous" decision
- **Key insight**: Honest uncertainty

### Case 4: Professional Deepfake (High Quality)
- Temporal signal is the key detector
- Multiple weak signals combine
- Explanation shows which signals failed

## Output Schema Design

```json
{
  "trust_score": 0.42,          // Single number for quick assessment
  "decision": "Ambiguous",       // Human-readable verdict
  "reason": "...",               // Detailed explanation
  "signals": {                   // Full breakdown for transparency
    "vision": { ... },
    "audio": { ... },
    "temporal": { ... }
  },
  "quality_assessment": { ... }, // Critical: shows input limitations
  "metadata": { ... }            // Context for interpretation
}
```

**Design principle**: Give humans everything they need to:
1. Understand the decision
2. Trust (or question) the result
3. Debug edge cases
4. Learn about deepfake characteristics

## Performance Characteristics

### Speed
- 10-second video: ~15-30 seconds analysis
- Bottlenecks:
  - Frame extraction: Linear with length
  - Optical flow: O(frames * pixels)
  - Audio analysis: Fast (~1 second)

### Accuracy (Estimated)
- **High Quality Real**: 85-95% correct classification
- **High Quality Fake**: 75-85% correct classification
- **Low Quality**: Correctly returns "Ambiguous"

**Note**: Accuracy is less important than **honest uncertainty**.

## Why This Approach Works

### 1. No Training Required
- Classical techniques only
- No dataset needed
- No GPU required
- Fast to implement

### 2. Explainable
- Every decision has a reason
- Signals are interpretable
- Humans can verify logic

### 3. Graceful Degradation
- Poor input → Low confidence
- Not "garbage in, confident output"
- Builds trust with users

### 4. Modular
- Easy to add new signals
- Easy to adjust weights
- Easy to debug individual components

### 5. Hackathon-Friendly
- Can be built in hours
- Impressive demonstrations
- Strong technical story
- Defensible decisions

## Demonstration Script

### Setup
1. Prepare 3 videos:
   - High quality real
   - Known deepfake
   - Compressed version of real video

### Demo Flow

**Video 1: High Quality Real**
- Upload → Analyze
- Point out: "All signals are strong (>0.7)"
- "Quality assessment is high (>0.8)"
- "Trust score: 0.85 - Real"

**Video 2: Known Deepfake**
- Upload → Analyze
- Point out: "Temporal signal is weak (<0.4)"
- "Multiple suspicious indicators"
- "Trust score: 0.28 - Fake"

**Video 3: Compressed Real**
- Upload → Analyze
- **KEY MOMENT**: Point out quality score (<0.5)
- "System reduces confidence - Ambiguous"
- **Say the line**: "Our system degrades confidence instead of hallucinating certainty"

### Impact
This demonstration shows:
- The system works (1 & 2)
- The system is smart (3)
- The system is trustworthy (3)

## Future Enhancements

### Short Term
- Face detection → region-specific analysis
- Lip-sync detection
- Blink pattern analysis

### Medium Term
- Multi-face tracking
- Per-segment analysis (timeline view)
- Confidence intervals

### Long Term
- GAN fingerprinting
- Source model detection
- Adversarial robustness testing

## Conclusion

This system embodies the principle:

> **Weak models + strong logic beats strong models + no logic**

By combining simple, explainable signals with intelligent quality-aware scoring, we create a system that is:
- Fast to build
- Easy to explain
- Honest about uncertainty
- Useful in practice

Perfect for hackathons. Perfect for building trust.
