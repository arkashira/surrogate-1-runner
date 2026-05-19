import axios from 'axios';

export const fetchFPSData = async () => {
  try {
    const response = await axios.get('https://api.example.com/benchmark');
    return response.data;
  } catch (error) {
    console.error('Error fetching FPS data:', error);
    throw error;
  }
};

// /opt/axentx/surrogate-1/src/components/FPSChart.jsx
import React, { useEffect, useState } from 'react';
import { fetchFPSData } from '../services/benchmarkService';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const FPSChart = () => {
  const [fpsData, setFPSData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchFPSData();
      setFPSData(data);
    };

    fetchData();

    // Auto-update on config change (e.g., window resize)
    window.addEventListener('resize', fetchData);

    return () => {
      window.removeEventListener('resize', fetchData);
    };
  }, []);

  if (!fpsData) {
    return <div>Loading...</div>;
  }

  const chartData = {
    labels: fpsData.times,
    datasets: [
      {
        label: 'FPS',
        data: fpsData.fps,
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  return <Line data={chartData} />;
};

export default FPSChart;