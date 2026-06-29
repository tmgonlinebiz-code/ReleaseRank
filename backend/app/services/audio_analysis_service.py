"""Audio analysis service for extracting real measurable metrics from audio files"""

import numpy as np
import librosa
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class AudioAnalysisService:
    """Service for analyzing audio files and extracting measurable metrics"""

    @staticmethod
    def analyze_file(file_path: str) -> Dict:
        """
        Analyze audio file and extract all metrics
        Returns dictionary with all audio metrics
        """
        try:
            # Load audio file
            y, sr = librosa.load(file_path, sr=None, mono=True)
            
            # Extract all metrics
            metrics = {
                "duration": AudioAnalysisService._get_duration(y, sr),
                "peak_level": AudioAnalysisService._get_peak_level(y),
                "rms_loudness": AudioAnalysisService._get_rms_loudness(y),
                "dynamic_range": AudioAnalysisService._get_dynamic_range(y),
                "bpm_estimate": AudioAnalysisService._estimate_bpm(y, sr),
                "spectral_balance": AudioAnalysisService._estimate_spectral_balance(y, sr),
                "energy_first_10s": AudioAnalysisService._get_energy_segment(y, sr, 0, 10),
                "energy_first_30s": AudioAnalysisService._get_energy_segment(y, sr, 0, 30),
                "clipping_detected": AudioAnalysisService._detect_clipping(y),
                "clipping_percentage": AudioAnalysisService._get_clipping_percentage(y),
                "retention_score": AudioAnalysisService._estimate_retention_score(y, sr),
            }
            
            return metrics
        
        except Exception as e:
            raise Exception(f"Audio analysis failed: {str(e)}")

    @staticmethod
    def _get_duration(y: np.ndarray, sr: int) -> float:
        """
        Get audio duration in seconds
        """
        return float(librosa.get_duration(y=y, sr=sr))

    @staticmethod
    def _get_peak_level(y: np.ndarray) -> float:
        """
        Get peak level (maximum absolute amplitude) in dB
        """
        peak_amplitude = np.max(np.abs(y))
        # Convert to dB (20 * log10(peak))
        if peak_amplitude > 0:
            peak_db = 20 * np.log10(peak_amplitude)
        else:
            peak_db = -np.inf
        return float(peak_db)

    @staticmethod
    def _get_rms_loudness(y: np.ndarray) -> float:
        """
        Get RMS (Root Mean Square) loudness in dB
        Measures overall perceived loudness
        """
        rms = np.sqrt(np.mean(y ** 2))
        if rms > 0:
            rms_db = 20 * np.log10(rms)
        else:
            rms_db = -np.inf
        return float(rms_db)

    @staticmethod
    def _get_dynamic_range(y: np.ndarray) -> float:
        """
        Estimate dynamic range (difference between peak and noise floor)
        Higher values = more dynamic (more variation)
        """
        # Calculate peak level
        peak = np.max(np.abs(y))
        
        # Calculate noise floor (quiet parts)
        # Sort absolute values and take bottom 10% as noise
        sorted_abs = np.sort(np.abs(y))
        noise_floor = np.mean(sorted_abs[:len(sorted_abs) // 10])
        
        if noise_floor > 0:
            dynamic_range = 20 * np.log10(peak / (noise_floor + 1e-10))
        else:
            dynamic_range = 0
        
        return float(np.clip(dynamic_range, 0, 100))  # Clip to reasonable range

    @staticmethod
    def _estimate_bpm(y: np.ndarray, sr: int) -> float:
        """
        Estimate BPM (tempo) using onset detection
        """
        try:
            # Extract onset strength
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            
            # Estimate tempo
            bpm = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
            
            return float(bpm[0]) if len(bpm) > 0 else 0.0
        except:
            return 0.0

    @staticmethod
    def _estimate_spectral_balance(y: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Estimate spectral balance (energy distribution across frequency bands)
        Returns proportions of energy in different frequency ranges
        """
        # Compute short-time Fourier transform
        S = np.abs(librosa.stft(y))
        
        # Get frequencies
        freqs = librosa.fft_frequencies(sr=sr, n_fft=S.shape[0] * 2 - 2)
        
        # Calculate total energy in each frequency band
        total_energy = np.sum(S ** 2)
        
        # Define frequency bands
        low_freq_energy = np.sum(S[freqs < 250] ** 2)
        mid_freq_energy = np.sum(S[(freqs >= 250) & (freqs < 4000)] ** 2)
        high_freq_energy = np.sum(S[freqs >= 4000] ** 2)
        
        # Normalize to percentages
        low_pct = float((low_freq_energy / (total_energy + 1e-10)) * 100)
        mid_pct = float((mid_freq_energy / (total_energy + 1e-10)) * 100)
        high_pct = float((high_freq_energy / (total_energy + 1e-10)) * 100)
        
        return {
            "low_freq_percent": low_pct,      # Below 250Hz
            "mid_freq_percent": mid_pct,      # 250Hz - 4kHz
            "high_freq_percent": high_pct,    # Above 4kHz
        }

    @staticmethod
    def _get_energy_segment(y: np.ndarray, sr: int, start_sec: float, end_sec: float) -> float:
        """
        Get energy (RMS loudness) for a specific time segment
        """
        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)
        
        # Clip to valid range
        start_sample = max(0, start_sample)
        end_sample = min(len(y), end_sample)
        
        if start_sample >= end_sample:
            return 0.0
        
        segment = y[start_sample:end_sample]
        rms = np.sqrt(np.mean(segment ** 2))
        
        if rms > 0:
            rms_db = 20 * np.log10(rms)
        else:
            rms_db = -np.inf
        
        return float(rms_db)

    @staticmethod
    def _detect_clipping(y: np.ndarray, threshold: float = 0.99) -> bool:
        """
        Detect if audio is clipping (samples at peak amplitude)
        """
        peak_count = np.sum(np.abs(y) > threshold)
        return bool(peak_count > 0)

    @staticmethod
    def _get_clipping_percentage(y: np.ndarray, threshold: float = 0.99) -> float:
        """
        Get percentage of samples that are clipping
        """
        if len(y) == 0:
            return 0.0
        
        clipping_count = np.sum(np.abs(y) > threshold)
        clipping_pct = (clipping_count / len(y)) * 100
        
        return float(np.clip(clipping_pct, 0, 100))

    @staticmethod
    def _estimate_retention_score(y: np.ndarray, sr: int) -> float:
        """
        Estimate retention score based on multiple factors:
        - Energy consistency throughout track
        - Low clipping detection
        - Balanced spectral content
        - Reasonable dynamic range
        
        Score: 0-100 (higher is better)
        """
        score = 100.0
        
        # Penalty for clipping
        clipping_pct = AudioAnalysisService._get_clipping_percentage(y)
        if clipping_pct > 0:
            score -= min(50, clipping_pct * 5)  # Max -50 points
        
        # Check energy consistency (divide into 3 segments)
        duration = AudioAnalysisService._get_duration(y, sr)
        if duration > 3:
            seg1_energy = AudioAnalysisService._get_energy_segment(y, sr, 0, duration / 3)
            seg2_energy = AudioAnalysisService._get_energy_segment(y, sr, duration / 3, 2 * duration / 3)
            seg3_energy = AudioAnalysisService._get_energy_segment(y, sr, 2 * duration / 3, duration)
            
            # If segments are vastly different, penalize
            energies = [seg1_energy, seg2_energy, seg3_energy]
            energy_std = np.std(energies)
            
            if energy_std > 5:  # More than 5dB variation
                score -= min(20, energy_std)  # Penalty based on variation
        
        # Bonus for good spectral balance (not too bass-heavy or treble-heavy)
        spectral = AudioAnalysisService._estimate_spectral_balance(y, sr)
        if 20 < spectral["low_freq_percent"] < 40 and spectral["high_freq_percent"] > 15:
            score += 5  # Small bonus for balanced spectrum
        
        # Bonus for good dynamic range
        dynamic_range = AudioAnalysisService._get_dynamic_range(y)
        if dynamic_range > 20:
            score += 5  # Bonus for good dynamics
        
        return float(np.clip(score, 0, 100))
