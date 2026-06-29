import React, { useState } from 'react';
import { useFileUpload } from '../hooks/useFileUpload';
import { useWorkflow } from '../hooks/useWorkflow';
import FileUpload from '../components/FileUpload';
import RankingResults from '../components/RankingResults';
import './UploadPage.css';

const UploadPage: React.FC<{ onWorkflowComplete?: () => void }> = ({ onWorkflowComplete }) => {
  const { uploadFiles, uploadProgress, uploadedFiles, isLoading: isUploading, deleteFile } = useFileUpload();
  const { analyzeAndRank, isLoading: isAnalyzing, results, error } = useWorkflow();
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileSelect = (files: File[]) => {
    setSelectedFiles(files);
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;
    await uploadFiles(selectedFiles);
    setSelectedFiles([]);
  };

  const handleAnalyze = async () => {
    if (uploadedFiles.length < 2) return;
    const fileIds = uploadedFiles.map(f => f.id);
    await analyzeAndRank(fileIds);
  };

  const handleDelete = async (fileId: string) => {
    try {
      await deleteFile(fileId);
    } catch (error) {
      console.error('Failed to delete file:', error);
    }
  };

  // Show results if analysis is complete
  if (results) {
    return (
      <RankingResults 
        results={results} 
        onReset={() => window.location.reload()}
      />
    );
  }

  return (
    <div className="upload-page">
      {/* Header */}
      <header className="page-header">
        <div className="header-content">
          <h1 className="page-title">🎵 ReleaseRank</h1>
          <p className="page-subtitle">Find your best mix version</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="page-main">
        {/* Upload Section */}
        <section className="upload-section">
          <div className="section-card">
            <h2 className="section-title">Step 1: Upload Audio Files</h2>
            <p className="section-description">Upload 2-10 versions of your track</p>
            
            <FileUpload 
              onFileSelect={handleFileSelect}
              disabled={isUploading || isAnalyzing}
            />
            
            {selectedFiles.length > 0 && (
              <button
                onClick={handleUpload}
                disabled={isUploading || isAnalyzing}
                className="btn btn-primary btn-upload"
              >
                {isUploading ? 'Uploading...' : `Upload ${selectedFiles.length} File${selectedFiles.length !== 1 ? 's' : ''}`}
              </button>
            )}
          </div>
        </section>

        {/* Upload Progress */}
        {uploadProgress.length > 0 && (
          <section className="progress-section">
            <div className="section-card">
              <h3 className="section-title">Upload Progress</h3>
              <div className="progress-list">
                {uploadProgress.map((item, index) => (
                  <div key={index} className="progress-item">
                    <div className="progress-header">
                      <span className="progress-name">{item.fileName}</span>
                      <span className={`progress-status status-${item.status}`}>
                        {item.status === 'success' && '✓'}
                        {item.status === 'error' && '✗'}
                        {item.status === 'uploading' && '...'}
                      </span>
                    </div>
                    <div className="progress-bar">
                      <div 
                        className={`progress-fill fill-${item.status}`}
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                    {item.error && <p className="progress-error">{item.error}</p>}
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Uploaded Files */}
        {uploadedFiles.length > 0 && (
          <section className="files-section">
            <div className="section-card">
              <h3 className="section-title">Uploaded Files ({uploadedFiles.length}/10)</h3>
              <div className="files-list">
                {uploadedFiles.map((file) => (
                  <div key={file.id} className="file-item">
                    <div className="file-info">
                      <div className="file-icon">🎵</div>
                      <div className="file-details">
                        <p className="file-name">{file.filename}</p>
                        <p className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDelete(file.id)}
                      className="btn-delete"
                      disabled={isAnalyzing}
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>

              {uploadedFiles.length >= 2 && (
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  className="btn btn-primary btn-analyze btn-large"
                >
                  {isAnalyzing ? 'Analyzing...' : `Analyze & Rank ${uploadedFiles.length} Files`}
                </button>
              )}
            </div>
          </section>
        )}

        {/* Error Message */}
        {error && (
          <section className="error-section">
            <div className="section-card error-card">
              <p className="error-text">❌ {error}</p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default UploadPage;
