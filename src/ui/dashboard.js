import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [costData, setCostData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/cloud-costs');
        setCostData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();

    // Set up real-time updates
    const interval = setInterval(fetchData, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Cloud Infrastructure Costs</h1>
      <div className="cost-data">
        {costData.map((item, index) => (
          <div key={index} className="cost-item">
            <p>Service: {item.service}</p>
            <p>Cost: ${item.cost.toFixed(2)}</p>
            <p>Time: {new Date(item.time).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;