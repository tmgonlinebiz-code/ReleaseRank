# Backend Documentation

## File Upload System

### Endpoints

#### POST /api/files/upload
Upload an audio file (MP3 or WAV)

**Request:**
- Form data with `file` field (multipart/form-data)
- Max file size: 50MB
- Allowed formats: MP3, WAV

**Response:**
```json
{
  "id": "uuid-string",
  "filename": "song.mp3",
  "file_type": "mp3",
  "size": 5242880,
  "uploaded_at": "2024-06-29T14:00:00Z",
  "message": "File uploaded successfully"
}
```

#### GET /api/files/list
List all uploaded audio files

**Response:**
```json
[
  {
    "id": "uuid-string",
    "filename": "song.mp3",
    "file_type": "mp3",
    "size": 5242880,
    "uploaded_at": "2024-06-29T14:00:00Z",
    "file_path": "uploads/uuid-string.mp3"
  }
]
```

#### GET /api/files/info/{file_id}
Get information about a specific uploaded file

**Response:** Same as list item above

#### DELETE /api/files/delete/{file_id}
Delete an uploaded audio file

**Response:**
```json
{
  "message": "File uuid-string deleted successfully",
  "file_id": "uuid-string"
}
```

### File Validation

- **Supported formats:** MP3, WAV
- **Maximum file size:** 50MB
- **Minimum file size:** 1KB
- **Validation errors:** Returned as 400 Bad Request with error detail

### File Storage

- Files are stored in the `uploads/` directory
- Each file is renamed with a UUID to avoid name conflicts
- Original filename is preserved in the database/registry
