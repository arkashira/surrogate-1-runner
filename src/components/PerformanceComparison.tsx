import React, { useState } from 'react';
import { GamePerformanceData } from '../types';

interface PerformanceComparisonProps {
  currentSetup: GamePerformanceData[];
  proposedSetup: GamePerformanceData[];
}

const PerformanceComparison: React.FC<PerformanceComparisonProps> = ({ currentSetup, proposedSetup }) => {
  const [showCurrent, setShowCurrent] = useState(true);

  const toggleSetup = () => {
    setShowCurrent(!showCurrent);
  };

  const calculateROI = (currentFPS: number, proposedFPS: number, componentCost: number) => {
    const fpsGain = proposedFPS - currentFPS;
    return (fpsGain / componentCost).toFixed(2);
  };

  return (
    <div className="performance-comparison">
      <div className="toggle-container">
        <button onClick={toggleSetup}>
          {showCurrent ? 'Show Proposed Setup' : 'Show Current Setup'}
        </button>
      </div>
      <div className="comparison-table">
        <table>
          <thead>
            <tr>
              <th>Game</th>
              <th>FPS</th>
              <th>Component</th>
              <th>ROI (FPS/$)</th>
            </tr>
          </thead>
          <tbody>
            {(showCurrent ? currentSetup : proposedSetup).map((gameData, index) => (
              <tr key={index}>
                <td>{gameData.game}</td>
                <td>{gameData.fps}</td>
                <td>{gameData.component}</td>
                <td>
                  {showCurrent
                    ? calculateROI(gameData.fps, proposedSetup[index].fps, gameData.cost)
                    : calculateROI(currentSetup[index].fps, gameData.fps, gameData.cost)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PerformanceComparison;