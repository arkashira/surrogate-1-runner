import React, { useEffect, useState } from 'react';
import { fetchRealWorldUsageData } from '../utils/realWorldUsage';

const ComponentDetails = ({ componentId }) => {
  const [usageData, setUsageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getUsageData = async () => {
      try {
        const data = await fetchRealWorldUsageData(componentId);
        setUsageData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    getUsageData();
  }, [componentId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Real-World Usage Data</h2>
      <pre>{JSON.stringify(usageData, null, 2)}</pre>
    </div>
  );
};

export default ComponentDetails;