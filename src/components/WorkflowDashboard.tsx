import React, { useState, useEffect } from 'react';
import { Tool } from '../types';

interface WorkflowDashboardProps {
  tools: Tool[];
  onAddTool: (tool: Tool) => void;
  onRemoveTool: (id: string) => void;
  onUpdateTool: (tool: Tool) => void;
}

const WorkflowDashboard: React.FC<WorkflowDashboardProps> = ({ tools, onAddTool, onRemoveTool, onUpdateTool }) => {
  const [newTool, setNewTool] = useState<Tool>({ id: '', name: '', status: 'inactive' });

  const handleAddTool = () => {
    onAddTool(newTool);
    setNewTool({ id: '', name: '', status: 'inactive' });
  };

  const handleRemoveTool = (id: string) => {
    onRemoveTool(id);
  };

  const handleUpdateTool = (tool: Tool) => {
    onUpdateTool(tool);
  };

  return (
    <div className="workflow-dashboard">
      <h1>Workflow Management Dashboard</h1>
      <div className="tool-list">
        {tools.map((tool) => (
          <div key={tool.id} className="tool-item">
            <span>{tool.name}</span>
            <span>{tool.status}</span>
            <button onClick={() => handleRemoveTool(tool.id)}>Remove</button>
            <button onClick={() => handleUpdateTool({ ...tool, status: tool.status === 'active' ? 'inactive' : 'active' })}>
              Toggle Status
            </button>
          </div>
        ))}
      </div>
      <div className="add-tool-form">
        <input
          type="text"
          placeholder="Tool Name"
          value={newTool.name}
          onChange={(e) => setNewTool({ ...newTool, name: e.target.value })}
        />
        <button onClick={handleAddTool}>Add Tool</button>
      </div>
    </div>
  );
};

export default WorkflowDashboard;