"""Pydantic request/response schemas"""

from pydantic import BaseModel
from datetime import datetime
from typing import List


class AudioFileBase(BaseModel):
    """Base audio file schema"""
    filename: str
    file_type: str


class AudioFileResponse(AudioFileBase):
    """Audio file response schema"""
    id: str
    size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class AnalysisResult(BaseModel):
    """Analysis result schema"""
    file_id: str
    youtube_score: float
    spotify_score: float
    recommendations: List[str] = []


class ComparisonRequest(BaseModel):
    """Comparison request schema"""
    file_ids: List[str]


class ComparisonResponse(BaseModel):
    """Comparison response schema"""
    results: List[AnalysisResult]
    winner_id: str
    comparison_summary: str