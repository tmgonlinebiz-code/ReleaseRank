"""Ranking and workflow routes"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ComparisonRequest, WorkflowResponse
from app.services.file_service import FileService
from app.services.audio_analysis_service import AudioAnalysisService
from app.services.ranking_service import RankingService

router = APIRouter(prefix="/workflow")


@router.post("/analyze-and-rank", response_model=WorkflowResponse)
async def analyze_and_rank(request: ComparisonRequest):
    """
    Complete workflow: Analyze multiple files and return ranking
    
    This is the main endpoint for the ReleaseRank workflow:
    1. Analyzes all uploaded files
    2. Calculates scores for each platform (YouTube, Spotify, Commercial)
    3. Ranks files from best to worst
    4. Returns winner with explanation and full ranking
    """
    if len(request.file_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 files required for comparison")
    
    if len(request.file_ids) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files for comparison")
    
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
    
    # Rank files
    try:
        winner, ranked = RankingService.rank_files(analyses)
        
        response = WorkflowResponse(
            winner=winner,
            ranked=ranked,
            total_files=len(request.file_ids)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking failed: {str(e)}")
