import React from 'react';
import { RankedFile } from '../types/index';
import './DetailedAnalysis.css';

interface DetailedAnalysisProps {
  file: RankedFile;
  onBack: () => void;
}

const DetailedAnalysis: React.FC<DetailedAnalysisProps> = ({ file, onBack }) => {
  const metrics = file.metrics;

  return (
    <div className="detailed-analysis">
      {/* Header */}
      <header className="analysis-header">
        <button onClick={onBack} className="back-button">← Back</button>
        <h1>Version {file.rank}</h1>
        <div></div>
      </header>

      {/* Main Content */}
      <main className="analysis-main">
        {/* Scores */}
        <section className="analysis-section">
          <h2 className="section-title">Scores</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-label">Overall</span>
              <span className="metric-value">{file.overall_score.toFixed(1)}</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">YouTube</span>
              <span className="metric-value">{file.youtube_score.toFixed(1)}</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Spotify</span>
              <span className="metric-value">{file.spotify_score.toFixed(1)}</span>
            </div>
            <div className="metric-card">
              <span className="metric-label">Mix</span>
              <span className="metric-value">{file.commercial_score.toFixed(1)}</span>
            </div>
          </div>
        </section>

        {/* Audio Metrics */}
        <section className="analysis-section">
          <h2 className="section-title">Technical Metrics</h2>
          <div className="tech-metrics">
            <div className="tech-row">
              <span className="tech-label">Duration</span>
              <span className="tech-value">{metrics.duration.toFixed(2)}s</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">Peak Level</span>
              <span className="tech-value">{metrics.peak_level.toFixed(2)} dB</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">RMS Loudness</span>
              <span className="tech-value">{metrics.rms_loudness.toFixed(2)} dB</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">Dynamic Range</span>
              <span className="tech-value">{metrics.dynamic_range.toFixed(2)} dB</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">BPM</span>
              <span className="tech-value">{metrics.bpm_estimate.toFixed(1)} BPM</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">First 10s Energy</span>
              <span className="tech-value">{metrics.energy_first_10s.toFixed(2)} dB</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">First 30s Energy</span>
              <span className="tech-value">{metrics.energy_first_30s.toFixed(2)} dB</span>
            </div>
            <div className="tech-row">
              <span className="tech-label">Clipping</span>
              <span className={`tech-value ${metrics.clipping_detected ? 'warning' : 'success'}`}>
                {metrics.clipping_detected ? `${metrics.clipping_percentage.toFixed(2)}%` : 'None'}
              </span>
            </div>
          </div>
        </section>

        {/* Spectral Balance */}
        <section className="analysis-section">
          <h2 className="section-title">Frequency Balance</h2>
          <div className="spectral-chart">
            <div className="frequency-bar">
              <div className="freq-segment low" style={{ width: `${metrics.spectral_balance.low_freq_percent}%` }}>
                <span className="freq-label">Low</span>
              </div>
              <div className="freq-segment mid" style={{ width: `${metrics.spectral_balance.mid_freq_percent}%` }}>
                <span className="freq-label">Mid</span>
              </div>
              <div className="freq-segment high" style={{ width: `${metrics.spectral_balance.high_freq_percent}%` }}>
                <span className="freq-label">High</span>
              </div>
            </div>
            <div className="frequency-labels">
              <div className="freq-info">
                <span className="freq-name">Bass</span>
                <span className="freq-value">{metrics.spectral_balance.low_freq_percent.toFixed(1)}%</span>
              </div>
              <div className="freq-info">
                <span className="freq-name">Mids</span>
                <span className="freq-value">{metrics.spectral_balance.mid_freq_percent.toFixed(1)}%</span>
              </div>
              <div className="freq-info">
                <span className="freq-name">Treble</span>
                <span className="freq-value">{metrics.spectral_balance.high_freq_percent.toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </section>

        {/* Retention Score */}
        <section className="analysis-section">
          <h2 className="section-title">Retention Potential</h2>
          <div className="retention-card">
            <div className="retention-meter">
              <div 
                className="retention-fill" 
                style={{ width: `${file.retention_score}%` }}
              />
            </div>
            <span className="retention-score">{file.retention_score.toFixed(1)}/100</span>
            <span className="retention-label">Listener retention potential</span>
          </div>
        </section>
      </main>
    </div>
  );
};

export default DetailedAnalysis;
