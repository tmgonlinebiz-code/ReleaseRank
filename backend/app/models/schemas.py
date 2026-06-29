"""Pydantic request/response schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


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


class AnalysisResult(BaseModel):
    """Analysis result schema"""
    file_id: str
    youtube_score: float = Field(..., ge=0, le=100)
    spotify_score: float = Field(..., ge=0, le=100)
    recommendations: List[str] = []


class ComparisonRequest(BaseModel):
    """Comparison request schema"""
    file_ids: List[str] = Field(..., min_items=2)


class ComparisonResponse(BaseModel):
    """Comparison response schema"""
    results: List[AnalysisResult]
    winner_id: str
    comparison_summary: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    status_code: int
