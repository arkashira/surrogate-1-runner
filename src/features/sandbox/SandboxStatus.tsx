import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState, AppDispatch } from '../../app/store';
import { fetchSandboxStatus } from './sandboxSlice';
import { useNavigate } from 'react-router-dom';

const statusMessages: Record<SandboxStatus, string> = {
  idle: 'Initiating sandbox creation...',
  creating: 'Creating your sandbox environment...',
  provisioning: 'Provisioning resources...',
  ready: 'Sandbox is ready!',
  error: 'An error occurred while creating your sandbox.',
};

export const SandboxStatus: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const status = useSelector((state: RootState) => state.sandbox.status);
  const error = useSelector((state: RootState) => state.sandbox.error);

  useEffect(() => {
    dispatch(fetchSandboxStatus());
  }, [dispatch]);

  const goToSandbox = () => navigate('/sandbox');

  return (
    <div className="sandbox-status">
      <h2>Sandbox Status</h2>
      <p>{statusMessages[status]}</p>
      {error && <p className="error">{error}</p>}
      {status === 'ready' && (
        <button onClick={goToSandbox}>Go to Sandbox</button>
      )}
    </div>
  );
};

export default SandboxStatus;