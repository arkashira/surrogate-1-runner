import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './EnvironmentController.css';

const EnvironmentController = () => {
  const [environmentState, setEnvironmentState] = useState('stopped');
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    const fetchEnvironmentState = async () => {
      try {
        const response = await axios.get('/api/environment/state');
        setEnvironmentState(response.data.state);
      } catch (error) {
        console.error('Error fetching environment state:', error);
      }
    };

    fetchEnvironmentState();
  }, []);

  const handleStartEnvironment = async () => {
    try {
      const response = await axios.post('/api/environment/start');
      setEnvironmentState('starting');
      setNotification('Environment is starting...');
      // Wait for environment to start
      await new Promise(resolve => setTimeout(resolve, 5000));
      setEnvironmentState('running');
      setNotification('Environment is running');
    } catch (error) {
      console.error('Error starting environment:', error);
      setNotification('Failed to start environment');
    }
  };

  const handleStopEnvironment = async () => {
    try {
      const response = await axios.post('/api/environment/stop');
      setEnvironmentState('stopping');
      setNotification('Environment is stopping...');
      // Wait for environment to stop
      await new Promise(resolve => setTimeout(resolve, 5000));
      setEnvironmentState('stopped');
      setNotification('Environment is stopped');
    } catch (error) {
      console.error('Error stopping environment:', error);
      setNotification('Failed to stop environment');
    }
  };

  return (
    <div className="environment-controller">
      <h2>Environment Controller</h2>
      <div className="environment-state">
        <p>Current State: {environmentState}</p>
      </div>
      <div className="environment-actions">
        {environmentState === 'stopped' && (
          <button onClick={handleStartEnvironment}>Start Environment</button>
        )}
        {environmentState === 'running' && (
          <button onClick={handleStopEnvironment}>Stop Environment</button>
        )}
      </div>
      {notification && <div className="notification">{notification}</div>}
    </div>
  );
};

export default EnvironmentController;