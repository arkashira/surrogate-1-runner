import React, { useState, useEffect } from 'react';
import SetupProgressBar from './components/SetupProgressBar';

const Setup = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Simulate progress update every 500ms
    const interval = setInterval(() => {
      setProgress((prevProgress) => (prevProgress < 100 ? prevProgress + 10 : 100));
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <SetupProgressBar progress={progress} />
      {/* Rest of the setup content */}
    </div>
  );
};

export default Setup;