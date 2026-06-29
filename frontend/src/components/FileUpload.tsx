import React, { useRef, useState } from 'react';

interface FileUploadProps {
  onFileSelect: (files: File[]) => void;
  disabled?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, disabled = false }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFiles = (files: FileList): File[] => {
    const validFiles: File[] = [];
    const allowedTypes = ['audio/mpeg', 'audio/wav'];
    const maxSize = 50 * 1024 * 1024; // 50MB

    Array.from(files).forEach((file) => {
      if (!allowedTypes.includes(file.type)) {
        alert(`Invalid file type: ${file.name}. Please upload MP3 or WAV files.`);
        return;
      }
      if (file.size > maxSize) {
        alert(`File too large: ${file.name}. Maximum size is 50MB.`);
        return;
      }
      validFiles.push(file);
    });

    return validFiles;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = validateFiles(e.dataTransfer.files);
    if (files.length > 0) {
      setSelectedFiles([...selectedFiles, ...files]);
      onFileSelect([...selectedFiles, ...files]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = validateFiles(e.target.files);
      if (files.length > 0) {
        setSelectedFiles([...selectedFiles, ...files]);
        onFileSelect([...selectedFiles, ...files]);
      }
    }
  };

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  };

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
    onFileSelect(newFiles);
  };

  return (
    <div className="w-full">
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        } ${
          disabled ? 'opacity-50 cursor-not-allowed' : ''
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="audio/mpeg,audio/wav"
          onChange={handleChange}
          className="hidden"
          disabled={disabled}
        />
        <div className="py-6">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-8-12l-4-4m0 0l-4 4m4-4v12"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <p className="mt-2 text-sm font-medium text-gray-900">
            Drag audio files here or click to select
          </p>
          <p className="mt-1 text-xs text-gray-500">
            Supported formats: MP3, WAV (Max 50MB per file)
          </p>
        </div>
      </div>

      {selectedFiles.length > 0 && (
        <div className="mt-6">
          <h3 className="text-sm font-medium text-gray-900 mb-3">Selected Files:</h3>
          <ul className="space-y-2">
            {selectedFiles.map((file, index) => (
              <li
                key={index}
                className="flex items-center justify-between bg-gray-50 p-3 rounded border border-gray-200"
              >
                <div className="flex items-center space-x-2">
                  <svg
                    className="h-5 w-5 text-gray-400"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9 2a2 2 0 00-2 2v8a2 2 0 002 2h5a2 2 0 002-2V4a2 2 0 00-2-2H9z" />
                  </svg>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(file.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  <svg
                    className="h-5 w-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
