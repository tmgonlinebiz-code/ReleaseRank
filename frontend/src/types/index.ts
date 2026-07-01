// Common type definitions

export interface AudioFile {
  id: string;
  filename: string;
  fileType: 'mp3' | 'wav';
  uploadedAt: Date;
  size: number;
}

export interface AnalysisResult {
  fileId: string;
  youtubeScore: number;
  spotifyScore: number;
  recommendations: string[];
}