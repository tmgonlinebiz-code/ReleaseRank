"""File upload and management routes"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import List
from app.models.schemas import AudioFileResponse, FileUploadResponse, ErrorResponse
from app.services.file_service import FileService
import json
import os

router = APIRouter(prefix="/files")

# In-memory storage for demo (replace with database)
upload_registry = {}


@router.post("/upload", response_model=FileUploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an audio file (MP3 or WAV)
    
    - **file**: Audio file to upload (max 50MB, MP3 or WAV format)
    """
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)

        # Validate file
        is_valid, error_msg = FileService.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Save file
        file_id, safe_filename, saved_size = FileService.save_file(file_content, file.filename)

        # Store file info
        file_info = FileService.get_file_info(file_id, file.filename, saved_size)
        upload_registry[file_id] = file_info

        return FileUploadResponse(
            id=file_id,
            filename=file.filename,
            file_type=file.filename.rsplit('.', 1)[1].lower(),
            size=saved_size,
            uploaded_at=file_info["uploaded_at"],
            message="File uploaded successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/list", response_model=List[AudioFileResponse])
async def list_files():
    """
    List all uploaded audio files
    """
    files = []
    for file_id, info in upload_registry.items():
        file_path = FileService.get_file_path(file_id)
        if file_path:
            files.append(AudioFileResponse(
                id=file_id,
                filename=info["filename"],
                file_type=info["file_type"],
                size=info["size"],
                uploaded_at=info["uploaded_at"],
                file_path=file_path
            ))
    return files


@router.get("/info/{file_id}", response_model=AudioFileResponse, responses={404: {"model": ErrorResponse}})
async def get_file_info(file_id: str):
    """
    Get information about a specific uploaded file
    """
    if file_id not in upload_registry:
        raise HTTPException(status_code=404, detail="File not found")

    info = upload_registry[file_id]
    file_path = FileService.get_file_path(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found on disk")

    return AudioFileResponse(
        id=file_id,
        filename=info["filename"],
        file_type=info["file_type"],
        size=info["size"],
        uploaded_at=info["uploaded_at"],
        file_path=file_path
    )


@router.delete("/delete/{file_id}", responses={404: {"model": ErrorResponse}})
async def delete_file(file_id: str):
    """
    Delete an uploaded audio file
    """
    if file_id not in upload_registry:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete from disk
    deleted = FileService.delete_file(file_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete file")

    # Remove from registry
    del upload_registry[file_id]

    return {"message": f"File {file_id} deleted successfully", "file_id": file_id}
