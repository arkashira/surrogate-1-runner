import React from 'react';
import './progress-dashboard.css';

const ProgressDashboard = () => {
  // Sample data, replace with actual data fetching
  const userProgress = {
    totalWords: 10000,
    correctWords: 8500,
    incorrectWords: 1500,
    streak: 7,
  };

  return (
    <div className="progress-dashboard">
      <h2>Progress Dashboard</h2>
      <div className="progress-stat">
        <span>Total Words:</span>
        <span>{userProgress.totalWords}</span>
      </div>
      <div className="progress-stat">
        <span>Correct Words:</span>
        <span>{userProgress.correctWords}</span>
      </div>
      <div className="progress-stat">
        <span>Incorrect Words:</span>
        <span>{userProgress.incorrectWords}</span>
      </div>
      <div className="progress-stat">
        <span>Streak:</span>
        <span>{userProgress.streak}</span>
      </div>
      <div className="recommendations">
        <h3>Recommendations:</h3>
        <ul>
          <li>Practice more to improve your streak.</li>
          <li>Review incorrect words to improve accuracy.</li>
        </ul>
      </div>
    </div>
  );
};

export default ProgressDashboard;