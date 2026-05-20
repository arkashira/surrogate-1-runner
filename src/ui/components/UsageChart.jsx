import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const UsageChart = ({ data }) => {
  const [filteredData, setFilteredData] = useState(data);
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedEndpoint, setSelectedEndpoint] = useState(null);

  useEffect(() => {
    if (selectedModel || selectedEndpoint) {
      const newData = data.filter(item => {
        return (!selectedModel || item.model === selectedModel) &&
               (!selectedEndpoint || item.endpoint === selectedEndpoint);
      });
      setFilteredData(newData);
    } else {
      setFilteredData(data);
    }
  }, [selectedModel, selectedEndpoint, data]);

  const models = [...new Set(data.map(item => item.model))];
  const endpoints = [...new Set(data.map(item => item.endpoint))];

  const chartData = {
    labels: filteredData.map(item => item.date),
    datasets: [
      {
        label: 'Tokens',
        data: filteredData.map(item => item.tokens),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      },
      {
        label: 'Cost',
        data: filteredData.map(item => item.cost),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  return (
    <div className="usage-chart">
      <div className="filters">
        <select onChange={(e) => setSelectedModel(e.target.value)} value={selectedModel || ''}>
          <option value="">All Models</option>
          {models.map(model => (
            <option key={model} value={model}>{model}</option>
          ))}
        </select>
        <select onChange={(e) => setSelectedEndpoint(e.target.value)} value={selectedEndpoint || ''}>
          <option value="">All Endpoints</option>
          {endpoints.map(endpoint => (
            <option key={endpoint} value={endpoint}>{endpoint}</option>
          ))}
        </select>
      </div>
      <div className="chart-container">
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default UsageChart;