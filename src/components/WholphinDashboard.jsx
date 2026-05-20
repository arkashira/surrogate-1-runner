import React, { useEffect, useState, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './WholphinDashboard.css';

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const WS_URL = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws/wholphin`;

const MAX_POINTS = 30; // keep last 30 seconds

const WholphinDashboard = () => {
  const [flashData, setFlashData] = useState<number[]>([]);
  const [bufferData, setBufferData] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  /* ---------- WebSocket ---------- */
  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      try {
        const { flashCount, bufferDuration } = JSON.parse(e.data);
        const timeLabel = new Date().toLocaleTimeString();

        setLabels((prev) => [...prev.slice(-MAX_POINTS + 1), timeLabel]);
        setFlashData((prev) => [...prev.slice(-MAX_POINTS + 1), flashCount]);
        setBufferData((prev) => [...prev.slice(-MAX_POINTS + 1), bufferDuration]);
      } catch (err) {
        console.error('Malformed WS payload', err);
      }
    };

    ws.onerror = (err) => console.error('WebSocket error', err);

    return () => {
      ws.close();
    };
  }, []);

  /* ---------- Chart data ---------- */
  const flashChartData = {
    labels,
    datasets: [
      {
        label: 'Flash Count',
        data: flashData,
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
        tension: 0.4,
      },
    ],
  };

  const bufferChartData = {
    labels,
    datasets: [
      {
        label: 'Buffer Duration (ms)',
        data: bufferData,
        borderColor: 'rgba(255,99,132,1)',
        backgroundColor: 'rgba(255,99,132,0.2)',
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: { beginAtZero: true },
    },
    plugins: {
      legend: { position: 'top' },
      title: { display: false },
    },
  };

  /* ---------- Render ---------- */
  return (
    <div className="dashboard-container">
      <h2>Wholphin Dashboard</h2>
      <div className="chart-wrapper">
        <Line data={flashChartData} options={options} />
      </div>
      <div className="chart-wrapper">
        <Line data={bufferChartData} options={options} />
      </div>
    </div>
  );
};

export default WholphinDashboard;