import { useState, useEffect } from 'react';
import { fetchIntegrationStatus } from '../api/integration';

export const useIntegrationStatus = () => {
  const [status, setStatus] = useState<string>('loading');
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const getStatus = async () => {
      try {
        const response = await fetchIntegrationStatus();
        setStatus(response.status);
      } catch (err) {
        setError(err as Error);
      }
    };

    getStatus();
  }, []);

  return { status, error };
};