import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ProgressTracker.css';

const ProgressTracker = ({ milestones, userProgress }) => {
  const [progress, setProgress] = useState(userProgress || {});

  useEffect(() => {
    // Save user progress to local storage
    localStorage.setItem('userProgress', JSON.stringify(progress));
  }, [progress]);

  const handleMilestoneClick = (milestone) => {
    setProgress((prev) => ({
      ...prev,
      [milestone]: true,
    }));
  };

  const completedMilestones = Object.keys(progress).filter((key) => progress[key]);
  const totalMilestones = milestones.length;

  return (
    <div className="progress-tracker">
      <div className="progress-bar">
        <div
          className="progress"
          style={{ width: `${(completedMilestones.length / totalMilestones) * 100}%` }}
        />
      </div>
      <ul className="milestones">
        {milestones.map((milestone, index) => (
          <li
            key={index}
            className={progress[milestone] ? 'completed' : 'pending'}
            onClick={() => handleMilestoneClick(milestone)}
          >
            {milestone}
          </li>
        ))}
      </ul>
    </div>
  );
};

ProgressTracker.propTypes = {
  milestones: PropTypes.arrayOf(PropTypes.string).isRequired,
  userProgress: PropTypes.object,
};

export default ProgressTracker;