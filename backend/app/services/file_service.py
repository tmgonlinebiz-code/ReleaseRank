"""File management service"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from app.core.constants import ALLOWED_AUDIO_FORMATS, MAX_FILE_SIZE, UPLOAD_DIR


class FileService:
    """Service for managing audio file uploads and storage"""

    @staticmethod
    def validate_file(filename: str, file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Validate audio file before upload
        Returns: (is_valid, error_message)
        """
        # Check file size
        if file_size > MAX_FILE_SIZE:
            return False, f"File size exceeds maximum of {MAX_FILE_SIZE / (1024*1024):.0f}MB"

        if file_size < 1024:
            return False, "File size must be at least 1KB"

        # Check file extension
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
        if not file_ext or file_ext not in ALLOWED_AUDIO_FORMATS:
            return False, f"Unsupported file format. Allowed: {', '.join(ALLOWED_AUDIO_FORMATS)}"

        return True, None

    @staticmethod
    def save_file(file_content: bytes, original_filename: str) -> Tuple[str, str, int]:
        """
        Save uploaded file to disk
        Returns: (file_id, file_path, file_size)
        """
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # Create safe filename
        safe_filename = f"{file_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)

        file_size = len(file_content)
        return file_id, safe_filename, file_size

    @staticmethod
    def get_file_path(file_id: str) -> Optional[str]:
        """
        Get full path to uploaded file by ID
        """
        upload_path = Path(UPLOAD_DIR)
        for file_path in upload_path.glob(f"{file_id}.*"):
            if file_path.is_file():
                return str(file_path)
        return None

    @staticmethod
    def delete_file(file_id: str) -> bool:
        """
        Delete uploaded file by ID
        """
        file_path = FileService.get_file_path(file_id)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def get_file_info(file_id: str, original_filename: str, file_size: int) -> dict:
        """
        Get file information dictionary
        """
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        return {
            "id": file_id,
            "filename": original_filename,
            "file_type": file_ext,
            "size": file_size,
            "uploaded_at": datetime.utcnow(),
        }
