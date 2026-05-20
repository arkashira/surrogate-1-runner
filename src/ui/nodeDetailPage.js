import React, { useState } from 'react';
import api from './api';

function NodeDetailPage({ nodeId }) {
  const [terminalError, setTerminalError] = useState(null);

  const handleLaunchTerminal = () => {
    try {
      const ws = api.launchTerminal(nodeId);
      // Handle successful terminal launch
    } catch (error) {
      setTerminalError(error.message);
    }
  };

  return (
    <div>
      <button onClick={handleLaunchTerminal}>Launch Terminal</button>
      {terminalError && (
        <div>
          <p>{terminalError}</p>
          <button onClick={handleLaunchTerminal}>Retry</button>
        </div>
      )}
    </div>
  );
}

export default NodeDetailPage;