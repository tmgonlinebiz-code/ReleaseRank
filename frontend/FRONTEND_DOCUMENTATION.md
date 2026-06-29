# ReleaseRank Frontend - File Upload System

## Components

### FileUpload Component

Reusable component for uploading audio files with drag-and-drop support.

**Props:**
- `onFileSelect`: Callback function when files are selected
- `disabled`: Optional boolean to disable upload functionality

**Features:**
- Drag and drop support
- File validation (type and size)
- Multiple file selection
- Remove individual files before upload
- Visual feedback for drag state

**Usage:**
```tsx
import FileUpload from './components/FileUpload';

<FileUpload 
  onFileSelect={(files) => setSelectedFiles(files)}
  disabled={isLoading}
/>
```

## Hooks

### useFileUpload Hook

Custom hook for managing file uploads with progress tracking.

**Returns:**
```typescript
{
  uploadFiles: (files: File[]) => Promise<void>,
  deleteFile: (fileId: string) => Promise<void>,
  clearProgress: () => void,
  uploadProgress: UploadProgress[],
  uploadedFiles: UploadedFile[],
  isLoading: boolean
}
```

**Features:**
- Upload multiple files
- Track upload progress
- Handle upload errors
- Delete uploaded files
- State management for upload status

**Usage:**
```tsx
const { uploadFiles, uploadProgress, uploadedFiles } = useFileUpload();

await uploadFiles(selectedFiles);
```

## API Service

### fileService

API client for file operations.

**Methods:**
- `upload(file: File)`: Upload a single file
- `list()`: Get all uploaded files
- `getInfo(fileId: string)`: Get file information
- `delete(fileId: string)`: Delete a file

**Configuration:**
- Base URL: `http://localhost:8000/api` (or from `REACT_APP_API_URL` env var)

## Environment Variables

```bash
# .env file
REACT_APP_API_URL=http://localhost:8000/api
```

## File Upload Flow

1. User selects files via FileUpload component
2. Files are validated on the client side
3. User clicks upload button
4. Files are uploaded to the backend via multipart/form-data
5. Backend validates and stores files
6. Progress is tracked and displayed
7. Uploaded files are listed in the table
8. User can delete files from the list
