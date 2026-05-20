import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

const Analytics = () => {
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'User Engagement',
        data: [],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  });

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      const response = await fetch('/api/analytics');
      const analyticsData = await response.json();
      const labels = analyticsData.map((dataPoint) => dataPoint.date);
      const userData = analyticsData.map((dataPoint) => dataPoint.users);
      setData({
        labels,
        datasets: [
          {
            label: 'User Engagement',
            data: userData,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
          },
        ],
      });
    };
    fetchAnalyticsData();
  }, []);

  return (
    <div>
      <Line data={data} />
    </div>
  );
};

export default Analytics;