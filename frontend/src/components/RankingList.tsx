import React from 'react';
import { RankedFile } from '../types/index';
import './RankingList.css';

interface RankingListProps {
  files: RankedFile[];
  onSelectFile: (file: RankedFile) => void;
}

const RankingList: React.FC<RankingListProps> = ({ files, onSelectFile }) => {
  return (
    <div className="ranking-list">
      {files.map((file, index) => (
        <div
          key={file.file_id}
          className="ranking-item"
          onClick={() => onSelectFile(file)}
        >
          <div className="ranking-number">
            {file.rank === 1 ? '🥇' : file.rank === 2 ? '🥈' : file.rank === 3 ? '🥉' : file.rank}
          </div>
          
          <div className="ranking-info">
            <h3 className="ranking-title">Version {file.rank}</h3>
            <div className="ranking-scores">
              <span className="mini-score">YouTube: {file.youtube_score.toFixed(0)}</span>
              <span className="mini-score">Spotify: {file.spotify_score.toFixed(0)}</span>
            </div>
          </div>
          
          <div className="ranking-overall">
            <span className="overall-score">{file.overall_score.toFixed(1)}</span>
          </div>
          
          <div className="ranking-arrow">→</div>
        </div>
      ))}
    </div>
  );
};

export default RankingList;
