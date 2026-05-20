import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { logEvent } from '../analytics/tracking';

const Dashboard = ({ userProgress, userFeedback }) => {
  const data = [
    { name: 'User Progress', uv: userProgress },
    { name: 'User Feedback', uv: userFeedback },
  ];

  const handleClick = (data) => {
    logEvent('Dashboard', 'Click', data.name);
  };

  return (
    <BarChart width={600} height={300} data={data} onClick={handleClick}>
      <Bar dataKey="uv" fill="#8884d8" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
    </BarChart>
  );
};

export default Dashboard;