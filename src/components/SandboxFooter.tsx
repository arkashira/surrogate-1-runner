import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

const SandboxFooter: React.FC = () => {
  const isFreeTier = useSelector((state: RootState) => state.user.isFreeTier);

  return (
    <div className="sandbox-footer">
      {isFreeTier && (
        <div className="watermark">
          <p>This is a free tier sandbox. Upgrade for full access.</p>
        </div>
      )}
      <p>© 2023 Axentx</p>
    </div>
  );
};

export default SandboxFooter;