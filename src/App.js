import React, { useState } from 'react';
import OnboardingTutorial from './components/OnboardingTutorial';

function App() {
  const [showTutorial, setShowTutorial] = useState(true);
  const [progress, setProgress] = useState(0);

  const skipTutorial = () => {
    setShowTutorial(false);
  };

  // Add API call demonstration and progress tracking here

  return (
    <div className="App">
      {showTutorial && <OnboardingTutorial skipTutorial={skipTutorial} progress={progress} />}
      {/* Rest of the app */}
    </div>
  );
}

export default App;