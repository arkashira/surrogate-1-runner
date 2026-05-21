import React, { useEffect, useState } from 'react';
import { Progress, Card } from 'antd';
import { getDataGenerationStatus } from '../services/dataService';

const DataGenerationStatus: React.FC = () => {
  const [status, setStatus] = useState<any>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      const data = await getDataGenerationStatus();
      setStatus(data);
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!status) {
    return <div>Loading...</div>;
  }

  return (
    <Card title="Data Generation Status">
      <Progress percent={status.progress} status={status.completed ? 'success' : 'active'} />
      <p>Generated: {status.generatedRecords} records</p>
      <p>Status: {status.completed ? 'Completed' : 'In Progress'}</p>
    </Card>
  );
};

export default DataGenerationStatus;