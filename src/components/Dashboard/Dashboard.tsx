import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Finding } from '../../types';
import { getFindings } from '../../services/api';

const Dashboard: React.FC = () => {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const data = await getFindings();
        setFindings(data);
      } catch (error) {
        console.error('Error fetching findings:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFindings();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Findings Dashboard</h1>
      <ul>
        {findings.map((finding) => (
          <li key={finding.id}>
            <Link to={`/dashboard/findings/${finding.id}`}>{finding.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;