import React, { useState } from 'react';

const VolumeSlider = ({ initialVolume = 1000, onChange }) => {
  const [volume, setVolume] = useState(initialVolume);

  const handleVolumeChange = (e) => {
    const newVolume = parseInt(e.target.value);
    setVolume(newVolume);
    if (onChange) onChange(newVolume);
  };

  const formatVolume = (value) => {
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}k`;
    }
    return value.toString();
  };

  return (
    <div className="volume-slider-container">
      <div className="volume-label">
        <span className="volume-value">{formatVolume(volume)}</span>
        <span className="volume-unit">records</span>
      </div>
      <input
        type="range"
        min="100"
        max="10000"
        step="100"
        value={volume}
        onChange={handleVolumeChange}
        className="volume-slider"
      />
      <div className="volume-range">
        <span>100</span>
        <span>10k</span>
      </div>
      <style jsx>{`
        .volume-slider-container {
          display: flex;
          flex-direction: column;
          width: 100%;
          max-width: 400px;
          margin: 20px 0;
        }
        .volume-label {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }
        .volume-value {
          font-size: 1.2rem;
          font-weight: bold;
          color: #4a5568;
        }
        .volume-unit {
          font-size: 0.9rem;
          color: #718096;
        }
        .volume-slider {
          width: 100%;
          height: 8px;
          border-radius: 4px;
          background: #e2e8f0;
          outline: none;
          -webkit-appearance: none;
        }
        .volume-slider::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #4299e1;
          cursor: pointer;
          transition: background 0.2s;
        }
        .volume-slider::-webkit-slider-thumb:hover {
          background: #3182ce;
        }
        .volume-slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #4299e1;
          cursor: pointer;
          transition: background 0.2s;
        }
        .volume-slider::-moz-range-thumb:hover {
          background: #3182ce;
        }
        .volume-range {
          display: flex;
          justify-content: space-between;
          margin-top: 5px;
          font-size: 0.8rem;
          color: #a0aec0;
        }
      `}</style>
    </div>
  );
};

export default VolumeSlider;