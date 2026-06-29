import { useState } from 'react'
import FileUpload from './components/FileUpload'
import { useFileUpload } from './hooks/useFileUpload'
import './App.css'

function App() {
  const { uploadFiles, deleteFile, uploadProgress, uploadedFiles, isLoading } = useFileUpload()
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])

  const handleFileSelect = (files: File[]) => {
    setSelectedFiles(files)
  }

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return
    await uploadFiles(selectedFiles)
    setSelectedFiles([])
  }

  const handleDelete = async (fileId: string) => {
    try {
      await deleteFile(fileId)
    } catch (error) {
      console.error('Failed to delete file:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900">🎵 ReleaseRank</h1>
              <p className="text-gray-600 mt-2">Compare audio files for YouTube and Spotify success</p>
            </div>
            <div className="text-right">
              <div className="inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
                {uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''} uploaded
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Audio Files</h2>
              <FileUpload 
                onFileSelect={handleFileSelect}
                disabled={isLoading}
              />
              
              {selectedFiles.length > 0 && (
                <button
                  onClick={handleUpload}
                  disabled={isLoading || selectedFiles.length === 0}
                  className="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition duration-200"
                >
                  {isLoading ? 'Uploading...' : `Upload ${selectedFiles.length} File${selectedFiles.length !== 1 ? 's' : ''}`}
                </button>
              )}
            </div>
          </div>

          {/* Stats Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Upload Statistics</h3>
            <div className="space-y-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Total Files</p>
                <p className="text-3xl font-bold text-blue-600">{uploadedFiles.length}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Ready for Analysis</p>
                <p className="text-3xl font-bold text-green-600">{uploadedFiles.length}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Total Size</p>
                <p className="text-3xl font-bold text-purple-600">
                  {(uploadedFiles.reduce((acc, f) => acc + f.size, 0) / (1024 * 1024)).toFixed(1)} MB
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Upload Progress */}
        {uploadProgress.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Upload Progress</h3>
            <div className="space-y-3">
              {uploadProgress.map((item, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900">{item.fileName}</span>
                    <span className={`text-xs font-medium ${
                      item.status === 'success' ? 'text-green-600' :
                      item.status === 'error' ? 'text-red-600' :
                      item.status === 'uploading' ? 'text-blue-600' :
                      'text-gray-600'
                    }`}>
                      {item.status === 'success' && '✓ Complete'}
                      {item.status === 'error' && '✗ Failed'}
                      {item.status === 'uploading' && 'Uploading...'}
                      {item.status === 'pending' && 'Pending'}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${
                        item.status === 'success' ? 'bg-green-600' :
                        item.status === 'error' ? 'bg-red-600' :
                        'bg-blue-600'
                      }`}
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                  {item.error && (
                    <p className="text-xs text-red-600 mt-1">{item.error}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Uploaded Files</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Filename</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Type</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Size</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Uploaded</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {uploadedFiles.map((file) => (
                    <tr key={file.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm text-gray-900">{file.filename}</td>
                      <td className="py-3 px-4 text-sm">
                        <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                          {file.file_type.toUpperCase()}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {new Date(file.uploaded_at).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4 text-sm">
                        <button
                          onClick={() => handleDelete(file.id)}
                          className="text-red-600 hover:text-red-800 font-medium"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
