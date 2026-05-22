import React from 'react';
import { ProgressBar } from 'react-bootstrap';
import './OnboardingTutorial.css';

const OnboardingTutorial = ({ skipTutorial, progress }) => {
  return (
    <div className="tutorial-container">
      <ProgressBar now={progress} label={`${progress}%`} />
      {/* Tutorial content goes here */}
      <button onClick={skipTutorial}>Skip Tutorial</button>
    </div>
  );
};

export default OnboardingTutorial;