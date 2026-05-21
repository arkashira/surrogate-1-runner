import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchWorkflows } from '../services/workflowService';

interface Agent {
  id: string;
  name: string;
  status: string;
}

interface Workflow {
  id: string;
  name: string;
  status: string;
  agents: Agent[];
}

interface WorkflowContextType {
  workflows: Workflow[];
  filterWorkflows: (filter: string) => void;
  sortWorkflows: (sortBy: string) => void;
}

const WorkflowContext = createContext<WorkflowContextType | undefined>(undefined);

export const WorkflowProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [filteredWorkflows, setFilteredWorkflows] = useState<Workflow[]>([]);

  useEffect(() => {
    const loadWorkflows = async () => {
      const data = await fetchWorkflows();
      setWorkflows(data);
      setFilteredWorkflows(data);
    };

    loadWorkflows();
    const interval = setInterval(loadWorkflows, 5000);

    return () => clearInterval(interval);
  }, []);

  const filterWorkflows = (filter: string) => {
    if (filter === '') {
      setFilteredWorkflows(workflows);
    } else {
      setFilteredWorkflows(workflows.filter(workflow => workflow.status === filter));
    }
  };

  const sortWorkflows = (sortBy: string) => {
    const sortedWorkflows = [...filteredWorkflows].sort((a, b) => {
      if (sortBy === 'name') {
        return a.name.localeCompare(b.name);
      } else if (sortBy === 'status') {
        return a.status.localeCompare(b.status);
      } else if (sortBy === 'date') {
        return new Date(a.id).getTime() - new Date(b.id).getTime();
      }
      return 0;
    });
    setFilteredWorkflows(sortedWorkflows);
  };

  return (
    <WorkflowContext.Provider value={{ workflows: filteredWorkflows, filterWorkflows, sortWorkflows }}>
      {children}
    </WorkflowContext.Provider>
  );
};

export const useWorkflowContext = () => {
  const context = useContext(WorkflowContext);
  if (!context) {
    throw new Error('useWorkflowContext must be used within a WorkflowProvider');
  }
  return context;
};