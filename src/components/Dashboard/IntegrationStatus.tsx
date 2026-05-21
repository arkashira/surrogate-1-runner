import React from 'react';
import { useIntegrationStatus } from '../../hooks/useIntegrationStatus';

const IntegrationStatus: React.FC = () => {
  const { status, error } = useIntegrationStatus();

  if (error) {
    return <div className="integration-status error">Error: {error.message}</div>;
  }

  if (status === 'loading') {
    return <div className="integration-status loading">Loading...</div>;
  }

  return (
    <div className="integration-status">
      <h3>Integration Status</h3>
      <p>Status: {status}</p>
    </div>
  );
};

export default IntegrationStatus;