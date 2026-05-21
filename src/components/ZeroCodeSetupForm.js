import React, { useState } from 'react';
import axios from 'axios';

const ZeroCodeSetupForm = () => {
  const [toolName, setToolName] = useState('');
  const [workflowName, setWorkflowName] = useState('');
  const [setupSuccess, setSetupSuccess] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    const setupData = {
      toolName,
      workflowName,
    };

    axios.post('/api/setup', setupData)
      .then((response) => {
        if (response.status === 200) {
          setSetupSuccess(true);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div>
      <h2>Zero-Code Setup</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Tool Name:
          <input type="text" value={toolName} onChange={(event) => setToolName(event.target.value)} />
        </label>
        <br />
        <label>
          Workflow Name:
          <input type="text" value={workflowName} onChange={(event) => setWorkflowName(event.target.value)} />
        </label>
        <br />
        <button type="submit">Setup</button>
      </form>
      {setupSuccess && <p>Setup successful!</p>}
    </div>
  );
};

export default ZeroCodeSetupForm;