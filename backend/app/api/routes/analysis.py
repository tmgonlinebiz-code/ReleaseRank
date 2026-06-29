"""Audio analysis routes"""

from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import AnalysisResult, AudioAnalysisResponse, ComparisonRequest, ComparisonResponse
from app.services.file_service import FileService
from app.services.audio_analysis_service import AudioAnalysisService

router = APIRouter(prefix="/analysis")

# In-memory storage for analysis results (replace with database)
analysis_cache = {}


@router.post("/analyze/{file_id}", response_model=AudioAnalysisResponse)
async def analyze_file(file_id: str):
    """
    Analyze a single audio file and extract measurable metrics
    
    Metrics returned:
    - duration: Duration in seconds
    - peak_level: Peak amplitude in dB
    - rms_loudness: Overall loudness in dB
    - dynamic_range: Variation in loudness (dB)
    - bpm_estimate: Estimated tempo (beats per minute)
    - spectral_balance: Energy distribution across frequency bands
    - energy_first_10s: Energy of first 10 seconds (dB)
    - energy_first_30s: Energy of first 30 seconds (dB)
    - clipping_detected: Whether audio is clipping
    - clipping_percentage: Percentage of samples clipping
    - retention_score: Estimated listener retention score (0-100)
    """
    # Check if analysis is cached
    if file_id in analysis_cache:
        return analysis_cache[file_id]
    
    # Get file path
    file_path = FileService.get_file_path(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")
    
    try:
        # Analyze audio file
        metrics = AudioAnalysisService.analyze_file(file_path)
        
        # Create response
        response = AudioAnalysisResponse(
            file_id=file_id,
            **metrics
        )
        
        # Cache result
        analysis_cache[file_id] = response
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/compare", response_model=dict)
async def compare_files(request: ComparisonRequest):
    """
    Compare multiple audio files based on analysis metrics
    
    Returns comparison results with ranked files
    """
    if len(request.file_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 files required for comparison")
    
    # Analyze all files
    analyses = []
    for file_id in request.file_ids:
        file_path = FileService.get_file_path(file_id)
        if not file_path:
            raise HTTPException(status_code=404, detail=f"File {file_id} not found")
        
        try:
            metrics = AudioAnalysisService.analyze_file(file_path)
            analyses.append({
                "file_id": file_id,
                "metrics": metrics
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed for {file_id}: {str(e)}")
    
    # Rank files by retention score (higher is better)
    ranked = sorted(analyses, key=lambda x: x["metrics"]["retention_score"], reverse=True)
    
    return {
        "analyses": analyses,
        "ranked": [
            {
                "rank": i + 1,
                "file_id": item["file_id"],
                "retention_score": item["metrics"]["retention_score"],
                "metrics": item["metrics"]
            }
            for i, item in enumerate(ranked)
        ],
        "winner_id": ranked[0]["file_id"],
        "winner_score": ranked[0]["metrics"]["retention_score"]
    }
