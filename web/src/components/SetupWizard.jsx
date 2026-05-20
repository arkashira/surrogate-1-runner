import React, { useState } from 'react';
import SuccessMessage from './SuccessMessage';

const SetupWizard = () => {
  const [isSetupComplete, setIsSetupComplete] = useState(false);

  const handleSetupComplete = () => {
    // Simulate setup completion
    setTimeout(() => {
      setIsSetupComplete(true);
    }, 30000); // 30 seconds
  };

  const handleCloseSuccessMessage = () => {
    // Handle closing the success message
    setIsSetupComplete(false);
  };

  return (
    <div className="setup-wizard">
      {!isSetupComplete && (
        <div>
          {/* Step 1: Select Model */}
          <h3>Select Model</h3>
          {/* Step 2: Set Data Size */}
          <h3>Set Data Size</h3>
          {/* Step 3: Confirm */}
          <h3>Confirm</h3>
          <button onClick={handleSetupComplete}>Complete Setup</button>
        </div>
      )}
      {isSetupComplete && (
        <SuccessMessage onClose={handleCloseSuccessMessage} />
      )}
    </div>
  );
};

export default SetupWizard;