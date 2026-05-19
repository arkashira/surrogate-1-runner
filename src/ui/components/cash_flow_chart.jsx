import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchForecastData } from '../../services/forecast_service';

const CashFlowChart = () => {
  const [forecastData, setForecastData] = useState([]);
  const [timeRange, setTimeRange] = useState('30-day');

  useEffect(() => {
    const loadForecastData = async () => {
      const data = await fetchForecastData(timeRange);
      setForecastData(data);
    };
    loadForecastData();
  }, [timeRange]);

  return (
    <div className="cash-flow-chart">
      <div className="chart-controls">
        <button onClick={() => setTimeRange('30-day')}>30-Day Forecast</button>
        <button onClick={() => setTimeRange('90-day')}>90-Day Forecast</button>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={forecastData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="cashFlow" stroke="#8884d8" name="Cash Flow" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CashFlowChart;