import { useState, useCallback } from 'react';
import { fileService } from '../services/api';

interface UploadProgress {
  fileId: string;
  fileName: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
}

interface UploadedFile {
  id: string;
  filename: string;
  file_type: string;
  size: number;
  uploaded_at: string;
}

export const useFileUpload = () => {
  const [uploadProgress, setUploadProgress] = useState<UploadProgress[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const uploadFiles = useCallback(
    async (files: File[]) => {
      setIsLoading(true);

      // Initialize progress tracking
      const initialProgress: UploadProgress[] = files.map((file) => ({
        fileId: `${file.name}-${Date.now()}`,
        fileName: file.name,
        status: 'pending',
        progress: 0,
      }));
      setUploadProgress(initialProgress);

      try {
        const uploadPromises = files.map(async (file, index) => {
          try {
            setUploadProgress((prev) =>
              prev.map((item, i) =>
                i === index ? { ...item, status: 'uploading', progress: 50 } : item
              )
            );

            const response = await fileService.upload(file);
            const uploadedFile = response.data;

            setUploadProgress((prev) =>
              prev.map((item, i) =>
                i === index
                  ? { ...item, status: 'success', progress: 100, fileId: uploadedFile.id }
                  : item
              )
            );

            setUploadedFiles((prev) => [...prev, uploadedFile]);
            return uploadedFile;
          } catch (error: any) {
            const errorMessage = error.response?.data?.detail || 'Upload failed';
            setUploadProgress((prev) =>
              prev.map((item, i) =>
                i === index
                  ? { ...item, status: 'error', progress: 0, error: errorMessage }
                  : item
              )
            );
            throw error;
          }
        });

        await Promise.allSettled(uploadPromises);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const deleteFile = useCallback(
    async (fileId: string) => {
      try {
        await fileService.delete(fileId);
        setUploadedFiles((prev) => prev.filter((file) => file.id !== fileId));
      } catch (error) {
        console.error('Failed to delete file:', error);
        throw error;
      }
    },
    []
  );

  const clearProgress = useCallback(() => {
    setUploadProgress([]);
  }, []);

  return {
    uploadFiles,
    deleteFile,
    clearProgress,
    uploadProgress,
    uploadedFiles,
    isLoading,
  };
};
