import React from 'react';
import { RankedFile } from '../types/index';
import './WinnerCard.css';

interface WinnerCardProps {
  winner: RankedFile;
}

const WinnerCard: React.FC<WinnerCardProps> = ({ winner }) => {
  return (
    <div className="winner-card">
      <div className="winner-badge">🥇 RECOMMENDED RELEASE</div>
      
      <div className="winner-content">
        <div className="score-main">
          <span className="score-label">Overall Score</span>
          <span className="score-value">{winner.overall_score.toFixed(1)}</span>
          <span className="score-max">/100</span>
        </div>

        <div className="scores-grid">
          <div className="score-box">
            <span className="score-box-label">YouTube</span>
            <span className="score-box-value">{winner.youtube_score.toFixed(0)}</span>
          </div>
          <div className="score-box">
            <span className="score-box-label">Spotify</span>
            <span className="score-box-value">{winner.spotify_score.toFixed(0)}</span>
          </div>
          <div className="score-box">
            <span className="score-box-label">Retention</span>
            <span className="score-box-value">{winner.retention_score.toFixed(0)}</span>
          </div>
          <div className="score-box">
            <span className="score-box-label">Mix</span>
            <span className="score-box-value">{winner.commercial_score.toFixed(0)}</span>
          </div>
        </div>

        <div className="confidence-section">
          <div className="confidence-meter">
            <div 
              className="confidence-bar" 
              style={{ width: `${winner.confidence}%` }}
            />
          </div>
          <span className="confidence-label">Confidence: {winner.confidence.toFixed(0)}%</span>
        </div>

        <div className="explanation">
          <p className="explanation-title">Why this version ranked first:</p>
          <p className="explanation-text">{winner.explanation}</p>
        </div>
      </div>
    </div>
  );
};

export default WinnerCard;
