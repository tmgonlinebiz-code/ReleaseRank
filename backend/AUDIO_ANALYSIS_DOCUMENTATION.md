# Audio Analysis Service Documentation

This module provides real measurable audio metrics from audio files without AI predictions.

## Metrics Extracted

### 1. Duration
- **Type**: Float (seconds)
- **Description**: Total duration of the audio file
- **Use**: Determining track length

### 2. Peak Level (dBFS)
- **Type**: Float (dB)
- **Description**: Maximum absolute amplitude in the audio signal
- **Range**: Typically -∞ to 0 dB
- **Use**: Detecting potential clipping and overall loudness ceiling

### 3. RMS Loudness (dBFS)
- **Type**: Float (dB)
- **Description**: Root Mean Square loudness - measures perceived overall loudness
- **Range**: Typically -60 to 0 dB
- **Use**: Comparing loudness between tracks

### 4. Dynamic Range (dB)
- **Type**: Float (0-100)
- **Description**: Difference between peak level and noise floor
- **Higher values**: More variation in loudness (more dynamic)
- **Lower values**: More consistent loudness (more compressed)
- **Use**: Assessing mix quality and musicality

### 5. BPM Estimate
- **Type**: Float (beats per minute)
- **Description**: Estimated tempo using onset detection
- **Range**: 0+ BPM
- **Use**: Understanding track pacing and rhythm

### 6. Spectral Balance
- **Type**: Dict with three frequencies
  - low_freq_percent: Energy below 250Hz
  - mid_freq_percent: Energy 250Hz-4kHz
  - high_freq_percent: Energy above 4kHz
- **Description**: Distribution of energy across frequency spectrum
- **Use**: Understanding frequency content and mix balance

### 7. Energy First 10 Seconds (dBFS)
- **Type**: Float (dB)
- **Description**: RMS loudness of the first 10 seconds
- **Use**: Assessing opening impact and hook quality

### 8. Energy First 30 Seconds (dBFS)
- **Type**: Float (dB)
- **Description**: RMS loudness of the first 30 seconds
- **Use**: Evaluating intro and opening energy

### 9. Clipping Detection
- **Type**: Boolean
- **Description**: Whether audio contains clipping (samples at maximum amplitude)
- **Use**: Quality control and distortion detection

### 10. Clipping Percentage
- **Type**: Float (0-100%)
- **Description**: Percentage of audio samples that are clipping
- **Threshold**: > 0.99 normalized amplitude
- **Use**: Quantifying the severity of clipping issues

### 11. Retention Score (0-100)
- **Type**: Float (0-100)
- **Description**: Estimated listener retention based on audio quality metrics
- **Factors**:
  - Penalty for clipping (up to -50 points)
  - Penalty for inconsistent energy across segments (up to -20 points)
  - Bonus for balanced spectral content (+5 points)
  - Bonus for good dynamic range (+5 points)
- **Use**: Quick quality assessment without AI

## API Endpoints

### POST /api/analysis/analyze/{file_id}
Analyze a single audio file

**Response**:
```json
{
  "file_id": "uuid",
  "duration": 180.5,
  "peak_level": -0.3,
  "rms_loudness": -15.2,
  "dynamic_range": 45.8,
  "bpm_estimate": 128.4,
  "spectral_balance": {
    "low_freq_percent": 35.2,
    "mid_freq_percent": 45.1,
    "high_freq_percent": 19.7
  },
  "energy_first_10s": -14.5,
  "energy_first_30s": -15.1,
  "clipping_detected": false,
  "clipping_percentage": 0.0,
  "retention_score": 85.3
}
```

### POST /api/analysis/compare
Compare multiple audio files

**Request**:
```json
{
  "file_ids": ["uuid1", "uuid2", "uuid3"]
}
```

**Response**:
```json
{
  "winner_id": "uuid1",
  "winner_score": 85.3,
  "ranked": [
    {
      "rank": 1,
      "file_id": "uuid1",
      "retention_score": 85.3,
      "metrics": { ... }
    }
  ]
}
```

## Libraries Used

- **librosa**: Audio analysis and feature extraction
- **numpy**: Numerical computations
- **scipy**: Scientific computing

## Future Enhancements

- AI-based platform predictions (YouTube/Spotify)
- Genre detection
- Mood/energy classification
- Advanced audio quality metrics
- Waveform visualization
- Frequency response graphs
