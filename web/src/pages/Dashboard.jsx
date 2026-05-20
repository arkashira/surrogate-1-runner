import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPipelines = async () => {
      try {
        const response = await axios.get('/api/pipelines');
        setPipelines(response.data);
        setLoading(false);
      } catch (error) {
        console.error(error);
      }
    };
    fetchPipelines();
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Running':
        return <span style={{ backgroundColor: 'blue', color: 'white', padding: '2px 4px', borderRadius: '4px' }}>{status}</span>;
      case 'Success':
        return <span style={{ backgroundColor: 'green', color: 'white', padding: '2px 4px', borderRadius: '4px' }}>{status}</span>;
      case 'Failed':
        return <span style={{ backgroundColor: 'red', color: 'white', padding: '2px 4px', borderRadius: '4px' }}>{status}</span>;
      default:
        return <span>{status}</span>;
    }
  };

  return (
    <div>
      <h1>Pipelines</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Pipeline Name</th>
              <th>Last Run Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {pipelines.map((pipeline) => (
              <tr key={pipeline.id}>
                <td>
                  <Link to={`/pipelines/${pipeline.id}`}>{pipeline.name}</Link>
                </td>
                <td>{pipeline.lastRunTime}</td>
                <td>{getStatusBadge(pipeline.status)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Dashboard;