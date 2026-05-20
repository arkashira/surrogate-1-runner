import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getInstanceData } from '../services/api';

const InstancePage = () => {
  const { instanceId } = useParams();
  const [instanceData, setInstanceData] = useState(null);

  useEffect(() => {
    const fetchInstanceData = async () => {
      const data = await getInstanceData(instanceId);
      setInstanceData(data);
    };

    fetchInstanceData();
  }, [instanceId]);

  if (!instanceData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="instance-page">
      <h1>{instanceData.name}</h1>
      <p>Total Data Size: {instanceData.totalDataSize}</p>
      {/* Other instance details */}
    </div>
  );
};

export default InstancePage;