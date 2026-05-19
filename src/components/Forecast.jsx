import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { forecast as computeForecast } from 'statsforecast'; // Using statsforecast library for ARIMA-based forecasting

const Forecast = ({ historicalData }) => {
  const [forecastData, setForecastData] = useState([]);
  const [errorMargin, setErrorMargin] = useState(0);

  useEffect(() => {
    if (historicalData && historicalData.length > 0) {
      // Compute 30-day forecast using ARIMA model
      const forecast = computeForecast(historicalData, { h: 30 });
      setForecastData(forecast);
      setErrorMargin(calculateErrorMargin(historicalData, forecast));
    }
  }, [historicalData]);

  const calculateErrorMargin = (actual, forecast) => {
    const lastActual = actual[actual.length - 1].value;
    const firstForecast = forecast[forecast.length - 30].value;
    return Math.abs((firstForecast - lastActual) / lastActual) * 100;
  };

  const exportToCSV = () => {
    const csvContent = [
      ['Day', 'Actual Cost', 'Forecasted Cost'],
      ...historicalData.map(d => [d.day, d.value, '']),
      ...forecastData.slice(historicalData.length).map(d => [d.day, '', d.value])
    ].map(row => row.join(',')).join('
');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'cost_forecast.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="forecast-container">
      <h2>Monthly Cost Forecast</h2>
      <p className="error-margin">Error Margin: {errorMargin.toFixed(2)}%</p>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={forecastData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" name="Actual Usage" />
          <Line type="monotone" dataKey="value" stroke="#82ca9d" name="Forecast" />
        </LineChart>
      </ResponsiveContainer>
      <button onClick={exportToCSV}>Export Forecast Data</button>
    </div>
  );
};

export default Forecast;