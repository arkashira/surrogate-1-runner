import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { Button } from './Button';

const SandboxHeader: React.FC = () => {
  const isFreeTier = useSelector((state: RootState) => state.user.isFreeTier);

  return (
    <div className="sandbox-header">
      <h1>Sandbox</h1>
      {isFreeTier && (
        <div className="free-tier-indicator">
          <span>Free Tier</span>
          <Button onClick={() => window.location.href = '/upgrade'}>Upgrade</Button>
        </div>
      )}
    </div>
  );
};

export default SandboxHeader;