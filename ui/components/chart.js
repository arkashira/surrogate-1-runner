import React, { useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const UsageChart = ({ data, anomalyThreshold = 1.5 }) => {
  const chartRef = useRef(null);
  
  useEffect(() => {
    if (chartRef.current) {
      const chart = chartRef.current;
      const ctx = chart.getContext('2d');
      const gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, 'rgba(54, 162, 235, 0.2)');
      gradient.addColorStop(1, 'rgba(54, 162, 235, 0)');
      
      chart.data = {
        labels: data.map(d => d.timestamp),
        datasets: [{
          label: 'LLM Usage',
          data: data.map(d => d.value),
          borderColor: 'rgb(54, 162, 235)',
          backgroundColor: gradient,
          tension: 0.4,
          fill: true,
          pointRadius: data.map(d => d.anomaly ? 6 : 3),
          pointBackgroundColor: data.map(d => d.anomaly ? 'red' : '#36a2eb')
        }]
      };
      
      chart.options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'LLM Usage Trends' },
          tooltip: {
            callbacks: {
              label: context => 
                `Value: ${context.parsed.y.toLocaleString()} tokens`
            }
          }
        },
        scales: {
          x: { 
            title: { display: true, text: 'Date' }
          },
          y: {
            title: { display: true, text: 'Tokens Used' },
            beginAtZero: true
          }
        }
      };
      
      chart.update();
    }
  }, [data, anomalyThreshold]);

  return <Line ref={chartRef} />;
};

export default UsageChart;