import React, { useEffect, useState } from 'react';
import { useWorkflowContext } from '../contexts/WorkflowContext';

interface LLMAgentStatusProps {
  agentId: string;
}

const LLMAgentStatus: React.FC<LLMAgentStatusProps> = ({ agentId }) => {
  const { workflows } = useWorkflowContext();
  const [status, setStatus] = useState<string>('Unknown');

  useEffect(() => {
    const updateStatus = () => {
      const workflow = workflows.find(w => w.agents.some(a => a.id === agentId));
      if (workflow) {
        const agent = workflow.agents.find(a => a.id === agentId);
        if (agent) {
          setStatus(agent.status);
        }
      }
    };

    updateStatus();
    const interval = setInterval(updateStatus, 5000);

    return () => clearInterval(interval);
  }, [agentId, workflows]);

  return (
    <div className={`status-indicator ${status.toLowerCase()}`}>
      {status}
    </div>
  );
};

export default LLMAgentStatus;