import React, { useState } from 'react';
import { AudioAnalysisResponse, RankedFile } from '../types/index';
import WinnerCard from './WinnerCard';
import RankingList from './RankingList';
import DetailedAnalysis from './DetailedAnalysis';
import './RankingResults.css';

interface RankingResultsProps {
  results: any;
  onReset: () => void;
}

const RankingResults: React.FC<RankingResultsProps> = ({ results, onReset }) => {
  const [selectedFile, setSelectedFile] = useState<any | null>(null);

  if (selectedFile) {
    return (
      <DetailedAnalysis 
        file={selectedFile}
        onBack={() => setSelectedFile(null)}
      />
    );
  }

  return (
    <div className="ranking-results">
      {/* Header */}
      <header className="results-header">
        <div className="header-content">
          <h1 className="header-title">🥇 Your Results</h1>
          <p className="header-subtitle">{results.total_files} versions analyzed</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="results-main">
        {/* Winner Section */}
        <section className="winner-section">
          <WinnerCard winner={results.winner} />
        </section>

        {/* All Rankings */}
        <section className="ranking-section">
          <div className="section-header">
            <h2>All Versions</h2>
          </div>
          <RankingList 
            files={results.ranked}
            onSelectFile={setSelectedFile}
          />
        </section>

        {/* Action Buttons */}
        <section className="action-section">
          <button onClick={onReset} className="btn btn-primary">
            Analyze New Files
          </button>
        </section>
      </main>
    </div>
  );
};

export default RankingResults;
