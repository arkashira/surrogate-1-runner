import React from 'react';
import SetupWizard from './SetupWizard';

const Dashboard = () => {
  const handleComplete = (data) => {
    console.log('Setup completed:', data);
    // Redirect or perform other actions after setup
  };

  const handleSkip = () => {
    console.log('Setup skipped!');
    // Handle skip action
  };

  return (
    <div>
      <h1>Main Dashboard</h1>
      <button onClick={() => console.log('Get Started button clicked!')}>Get Started</button>
      <SetupWizard onComplete={handleComplete} onSkip={handleSkip} />
    </div>
  );
};

export default Dashboard;