"""Application constants"""

import os

# File upload settings
ALLOWED_AUDIO_FORMATS = {'mp3', 'wav'}
MAX_FILE_SIZE = 52428800  # 50MB in bytes
MIN_FILE_SIZE = 1024  # 1KB in bytes

# Upload directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
