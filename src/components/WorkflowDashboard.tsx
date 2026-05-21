import React from 'react';
import { useWorkflowContext } from '../contexts/WorkflowContext';
import LLMAgentStatus from './LLMAgentStatus';

const WorkflowDashboard: React.FC = () => {
  const { workflows, filterWorkflows, sortWorkflows } = useWorkflowContext();

  const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    filterWorkflows(e.target.value);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    sortWorkflows(e.target.value);
  };

  return (
    <div className="workflow-dashboard">
      <div className="dashboard-controls">
        <select onChange={handleFilterChange}>
          <option value="">All Workflows</option>
          <option value="active">Active Workflows</option>
          <option value="completed">Completed Workflows</option>
          <option value="failed">Failed Workflows</option>
        </select>
        <select onChange={handleSortChange}>
          <option value="name">Sort by Name</option>
          <option value="status">Sort by Status</option>
          <option value="date">Sort by Date</option>
        </select>
      </div>
      <div className="workflow-list">
        {workflows.map(workflow => (
          <div key={workflow.id} className="workflow-item">
            <h3>{workflow.name}</h3>
            <div className="agent-list">
              {workflow.agents.map(agent => (
                <div key={agent.id} className="agent-item">
                  <span>{agent.name}</span>
                  <LLMAgentStatus agentId={agent.id} />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WorkflowDashboard;