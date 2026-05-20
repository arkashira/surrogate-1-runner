import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import budgetService from '../services/budgetService';

const BudgetWidget = () => {
  const [data, setData] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [confidenceInterval, setConfidenceInterval] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await budgetService.getHistoricalData();
      setData(response.data);
    };
    fetchData();
  }, []);

  const handleForecast = async () => {
    const response = await budgetService.getForecast(data);
    setForecast(response.forecast);
    setConfidenceInterval(response.confidenceInterval);
  };

  const handleAdjustParameters = async (params) => {
    const response = await budgetService.adjustForecastParams(params);
    setForecast(response.forecast);
    setConfidenceInterval(response.confidenceInterval);
  };

  return (
    <div>
      <h2>Budget Forecast</h2>
      <LineChart width={500} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis dataKey="cost" />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="cost" stroke="#8884d8" activeDot={{ r: 8 }} />
        {forecast.length > 0 && (
          <Line type="monotone" dataKey="forecast" stroke="#82ca9d" activeDot={{ r: 8 }} />
        )}
        {confidenceInterval.length > 0 && (
          <Line type="monotone" dataKey="confidenceInterval" stroke="#ccc" activeDot={{ r: 8 }} />
        )}
      </LineChart>
      <button onClick={handleForecast}>Generate Forecast</button>
      <button onClick={() => handleAdjustParameters({ param1: 'value1', param2: 'value2' })}>
        Adjust Parameters
      </button>
    </div>
  );
};

export default BudgetWidget;