import { useState, useEffect } from 'react';
import axios from 'axios';

interface Anomaly {
  id: number;
  name: string;
  severity: string;
  type: string;
  startTime: string;
  endTime: string;
}

const useAnomalies = () => {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnomalies = async () => {
      try {
        const response = await axios.get('/api/anomalies');
        setAnomalies(response.data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnomalies();
  }, []);

  return { anomalies, loading, error };
};

export default useAnomalies;