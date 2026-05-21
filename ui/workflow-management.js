import React, { useState, useEffect } from 'react';
import axios from 'axios';

const WorkflowManagement = () => {
  const [workflows, setWorkflows] = useState([]);

  useEffect(() => {
    const fetchWorkflows = async () => {
      const response = await axios.get('/api/workflows');
      setWorkflows(response.data);
    };

    fetchWorkflows();
  }, []);

  const handleCreateWorkflow = async () => {
    // Implement create workflow logic here
  };

  const handleDeleteWorkflow = async (workflowId) => {
    // Implement delete workflow logic here
  };

  return (
    <div>
      <h1>Workflow Management</h1>
      <button onClick={handleCreateWorkflow}>Create Workflow</button>
      <ul>
        {workflows.map((workflow) => (
          <li key={workflow.id}>
            {workflow.name}
            <button onClick={() => handleDeleteWorkflow(workflow.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WorkflowManagement;