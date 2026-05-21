import React, { useState } from 'react';
import WorkflowDashboard from './components/WorkflowDashboard';
import { Tool } from './types';

const App: React.FC = () => {
  const [tools, setTools] = useState<Tool[]>([]);

  const handleAddTool = (tool: Tool) => {
    setTools([...tools, { ...tool, id: Date.now().toString() }]);
  };

  const handleRemoveTool = (id: string) => {
    setTools(tools.filter((tool) => tool.id !== id));
  };

  const handleUpdateTool = (updatedTool: Tool) => {
    setTools(tools.map((tool) => (tool.id === updatedTool.id ? updatedTool : tool)));
  };

  return (
    <div className="App">
      <WorkflowDashboard
        tools={tools}
        onAddTool={handleAddTool}
        onRemoveTool={handleRemoveTool}
        onUpdateTool={handleUpdateTool}
      />
    </div>
  );
};

export default App;