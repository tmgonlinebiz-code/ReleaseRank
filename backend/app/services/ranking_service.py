"""Service for ranking and comparing audio files"""

import numpy as np
from typing import List, Dict, Tuple
from app.services.audio_analysis_service import AudioAnalysisService


class RankingService:
    """Service for ranking audio files based on multiple scoring criteria"""

    @staticmethod
    def calculate_youtube_score(metrics: Dict) -> float:
        """
        Calculate YouTube success score (0-100)
        YouTube prioritizes: engagement, watch time, retention
        
        Factors:
        - Strong opening (first 10s energy)
        - Good dynamic range (keeps listeners engaged)
        - Moderate loudness (not too quiet or clipping)
        - Balanced spectral content (good mix)
        """
        score = 50.0  # Base score
        
        # Strong opening (first 10s energy)
        energy_first_10 = metrics["energy_first_10s"]
        if energy_first_10 > -20:  # Good opening
            score += 15
        elif energy_first_10 > -25:  # Decent opening
            score += 8
        elif energy_first_10 < -35:  # Weak opening
            score -= 10
        
        # Dynamic range (keeps engagement)
        dynamic = metrics["dynamic_range"]
        if 25 < dynamic < 50:
            score += 12
        elif dynamic > 50:
            score += 8  # Very dynamic is good
        elif dynamic < 15:
            score -= 8  # Too compressed
        
        # Clipping penalty (major issue)
        if metrics["clipping_detected"]:
            score -= min(30, metrics["clipping_percentage"] * 3)
        
        # RMS loudness (should be competitive)
        loudness = metrics["rms_loudness"]
        if -12 < loudness < -6:
            score += 10
        elif -15 < loudness < -12:
            score += 5
        elif loudness < -20:
            score -= 10
        
        # Spectral balance (good mixes have balanced frequencies)
        spectral = metrics["spectral_balance"]
        if 25 < spectral["mid_freq_percent"] < 55:
            score += 8
        
        return float(np.clip(score, 0, 100))

    @staticmethod
    def calculate_spotify_score(metrics: Dict) -> float:
        """
        Calculate Spotify success score (0-100)
        Spotify prioritizes: consistency, stream finish rate, playlist fit
        
        Factors:
        - Consistent energy throughout (finish rate)
        - No clipping (clean audio)
        - Moderate peak levels
        - Good sustained energy in first 30s
        """
        score = 50.0  # Base score
        
        # First 30s sustained energy (playlist hook)
        energy_first_30 = metrics["energy_first_30s"]
        if -15 < energy_first_30 < -8:
            score += 15
        elif -18 < energy_first_30 < -15:
            score += 8
        elif energy_first_30 < -25:
            score -= 15
        
        # No clipping (stream quality)
        if not metrics["clipping_detected"]:
            score += 15
        else:
            score -= min(25, metrics["clipping_percentage"] * 2.5)
        
        # Peak level (broadcast standard compliance)
        peak = metrics["peak_level"]
        if -3 < peak < -0.1:
            score += 12
        elif peak <= -3:
            score += 5  # A bit quiet but safe
        elif peak > -0.1:
            score -= 20  # Clipping risk
        
        # RMS consistency
        loudness = metrics["rms_loudness"]
        if -13 < loudness < -8:
            score += 10  # Spotify sweet spot
        
        # Dynamic range (some dynamics good, not too extreme)
        dynamic = metrics["dynamic_range"]
        if 15 < dynamic < 45:
            score += 8
        elif dynamic > 50:
            score += 3  # Too much variation
        
        return float(np.clip(score, 0, 100))

    @staticmethod
    def calculate_commercial_mix_score(metrics: Dict) -> float:
        """
        Calculate Commercial Mix score (0-100)
        Represents overall mix quality and commercial viability
        
        Factors:
        - No clipping
        - Good loudness levels
        - Balanced spectral content
        - Reasonable dynamic range
        """
        score = 50.0  # Base score
        
        # Clipping is major issue for commercial
        if metrics["clipping_detected"]:
            score -= min(40, metrics["clipping_percentage"] * 4)
        else:
            score += 15
        
        # Loudness level
        loudness = metrics["rms_loudness"]
        if -14 < loudness < -8:
            score += 15  # Commercial sweet spot
        elif -16 < loudness < -14:
            score += 8
        elif loudness > -8 or loudness < -18:
            score -= 10
        
        # Peak level
        peak = metrics["peak_level"]
        if -6 < peak < -1:
            score += 10
        
        # Spectral balance (commercial mixes are balanced)
        spectral = metrics["spectral_balance"]
        low = spectral["low_freq_percent"]
        mid = spectral["mid_freq_percent"]
        high = spectral["high_freq_percent"]
        
        # Ideal: 30% low, 45% mid, 25% high
        balance_score = 20 - (abs(low - 30) + abs(mid - 45) + abs(high - 25)) / 5
        score += max(0, balance_score)
        
        # Dynamic range (professional mixes have good dynamics)
        dynamic = metrics["dynamic_range"]
        if 20 < dynamic < 50:
            score += 10
        
        return float(np.clip(score, 0, 100))

    @staticmethod
    def calculate_overall_score(youtube: float, spotify: float, commercial: float) -> float:
        """
        Calculate weighted overall score
        """
        # Weights: YouTube 40%, Spotify 40%, Commercial 20%
        overall = (youtube * 0.4) + (spotify * 0.4) + (commercial * 0.2)
        return float(np.clip(overall, 0, 100))

    @staticmethod
    def rank_files(files_data: List[Dict]) -> Tuple[Dict, List[Dict]]:
        """
        Rank files and return winner plus full ranking
        
        Args:
            files_data: List of dicts with 'file_id' and 'metrics'
        
        Returns:
            Tuple of (winner_info, ranked_list)
        """
        ranked = []
        
        for item in files_data:
            file_id = item["file_id"]
            metrics = item["metrics"]
            
            # Calculate scores
            youtube_score = RankingService.calculate_youtube_score(metrics)
            spotify_score = RankingService.calculate_spotify_score(metrics)
            commercial_score = RankingService.calculate_commercial_mix_score(metrics)
            overall_score = RankingService.calculate_overall_score(
                youtube_score, spotify_score, commercial_score
            )
            
            # Get explanation
            explanation = RankingService._generate_explanation(
                metrics, youtube_score, spotify_score, commercial_score
            )
            
            ranked_item = {
                "file_id": file_id,
                "overall_score": overall_score,
                "youtube_score": youtube_score,
                "spotify_score": spotify_score,
                "commercial_score": commercial_score,
                "retention_score": metrics["retention_score"],
                "confidence": RankingService._calculate_confidence(metrics),
                "explanation": explanation,
                "metrics": metrics
            }
            
            ranked.append(ranked_item)
        
        # Sort by overall score (highest first)
        ranked.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Add rank
        for i, item in enumerate(ranked):
            item["rank"] = i + 1
        
        # Winner is first
        winner = ranked[0].copy()
        
        return winner, ranked

    @staticmethod
    def _generate_explanation(metrics: Dict, youtube: float, spotify: float, commercial: float) -> str:
        """
        Generate short explanation for why this file ranked well
        """
        reasons = []
        
        # Check for strengths
        if not metrics["clipping_detected"]:
            reasons.append("Clean audio with no clipping")
        
        if -14 < metrics["rms_loudness"] < -8:
            reasons.append("Commercial loudness level")
        
        if metrics["dynamic_range"] > 25:
            reasons.append("Good dynamic range")
        
        if metrics["retention_score"] > 80:
            reasons.append("High retention potential")
        
        if metrics["energy_first_10s"] > -20:
            reasons.append("Strong opening hook")
        
        # Pick top 2-3 reasons
        explanation = " | ".join(reasons[:3]) if reasons else "Solid overall mix"
        
        return explanation

    @staticmethod
    def _calculate_confidence(metrics: Dict) -> float:
        """
        Calculate confidence score (0-100) for the ranking
        Based on audio quality metrics consistency
        """
        confidence = 85.0  # Base confidence
        
        # Reduce confidence if clipping detected
        if metrics["clipping_detected"]:
            confidence -= 20
        
        # Reduce confidence if very quiet
        if metrics["rms_loudness"] < -25:
            confidence -= 10
        
        # Reduce confidence if very short
        if metrics["duration"] < 5:
            confidence -= 15
        
        return float(np.clip(confidence, 0, 100))
