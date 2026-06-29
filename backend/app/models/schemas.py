"""Pydantic request/response schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict


class AudioFileBase(BaseModel):
    """Base audio file schema"""
    filename: str = Field(..., min_length=1, max_length=255)
    file_type: str = Field(..., pattern="^(mp3|wav)$")


class AudioFileResponse(AudioFileBase):
    """Audio file response schema"""
    id: str
    size: int = Field(..., gt=0)
    uploaded_at: datetime
    file_path: str

    class Config:
        from_attributes = True


class AudioFileList(BaseModel):
    """List of audio files"""
    files: List[AudioFileResponse]
    total: int


class FileUploadResponse(BaseModel):
    """File upload response"""
    id: str
    filename: str
    file_type: str
    size: int
    uploaded_at: datetime
    message: str = "File uploaded successfully"


class SpectralBalance(BaseModel):
    """Spectral balance metrics"""
    low_freq_percent: float = Field(..., ge=0, le=100, description="Energy below 250Hz (%)")
    mid_freq_percent: float = Field(..., ge=0, le=100, description="Energy 250Hz-4kHz (%)")
    high_freq_percent: float = Field(..., ge=0, le=100, description="Energy above 4kHz (%)")


class AudioAnalysisResponse(BaseModel):
    """Complete audio analysis response with measurable metrics"""
    file_id: str
    duration: float = Field(..., ge=0, description="Duration in seconds")
    peak_level: float = Field(..., description="Peak amplitude in dB")
    rms_loudness: float = Field(..., description="RMS loudness in dB")
    dynamic_range: float = Field(..., ge=0, le=100, description="Dynamic range in dB")
    bpm_estimate: float = Field(..., ge=0, description="Estimated tempo (BPM)")
    spectral_balance: SpectralBalance = Field(..., description="Frequency energy distribution")
    energy_first_10s: float = Field(..., description="Energy of first 10 seconds (dB)")
    energy_first_30s: float = Field(..., description="Energy of first 30 seconds (dB)")
    clipping_detected: bool = Field(..., description="Whether audio contains clipping")
    clipping_percentage: float = Field(..., ge=0, le=100, description="Percentage of samples clipping")
    retention_score: float = Field(..., ge=0, le=100, description="Estimated listener retention score")


class AnalysisResult(BaseModel):
    """Analysis result schema"""
    file_id: str
    youtube_score: float = Field(..., ge=0, le=100)
    spotify_score: float = Field(..., ge=0, le=100)
    recommendations: List[str] = []


class ComparisonRequest(BaseModel):
    """Comparison request schema"""
    file_ids: List[str] = Field(..., min_items=2, max_items=10)


class RankedFile(BaseModel):
    """Ranked file in the results"""
    rank: int = Field(..., ge=1, le=10)
    file_id: str
    overall_score: float = Field(..., ge=0, le=100)
    youtube_score: float = Field(..., ge=0, le=100)
    spotify_score: float = Field(..., ge=0, le=100)
    commercial_score: float = Field(..., ge=0, le=100)
    retention_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=100)
    explanation: str
    metrics: AudioAnalysisResponse


class WorkflowResponse(BaseModel):
    """Complete workflow response with ranking"""
    winner: RankedFile = Field(..., description="Best ranked file")
    ranked: List[RankedFile] = Field(..., description="All files ranked from best to worst")
    total_files: int = Field(..., ge=2, le=10)


class ComparisonResponse(BaseModel):
    """Comparison response schema"""
    results: List[AnalysisResult]
    winner_id: str
    comparison_summary: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int
