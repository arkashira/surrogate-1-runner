import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './forecast.css';

/**
 * ForecastChart Component
 * Displays 7-day and 30-day cost forecasts.
 *
 * Props:
 * - data: Array of objects containing date, 7dayForecast, and 30dayForecast.
 * - title: Optional string for the chart title.
 */
const ForecastChart = ({ data, title = 'Cost Forecast' }) => {
  // Handle empty or missing data state (Best practice from Candidate 2)
  if (!data || data.length === 0) {
    return (
      <div className="forecast-chart">
        <h3 className="forecast-chart__title">{title}</h3>
        <div className="forecast-chart__empty">No forecast data available.</div>
      </div>
    );
  }

  return (
    <div className="forecast-chart">
      <h3 className="forecast-chart__title">{title}</h3>
      
      {/* ResponsiveContainer ensures the chart fits any screen size (Best practice from Candidate 2) */}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          
          {/* XAxis formatted to show MM-DD for cleaner look */}
          <XAxis 
            dataKey="date" 
            tickFormatter={(tick) => tick.slice(5, 10)} 
          />
          
          <YAxis />
          
          {/* Tooltip formatted as currency (Best practice from Candidate 2) */}
          <Tooltip
            formatter={(value) => [`$${value.toFixed(2)}`, 'Cost']}
            labelFormatter={(label) => `Date: ${label}`}
          />
          
          <Legend />
          
          {/* 7-Day Forecast Line (Specific requirement from Candidate 1) */}
          <Line
            type="monotone"
            dataKey="7dayForecast"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
            name="7-Day Forecast"
          />
          
          {/* 30-Day Forecast Line (Specific requirement from Candidate 1) */}
          <Line
            type="monotone"
            dataKey="30dayForecast"
            stroke="#82ca9d"
            name="30-Day Forecast"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ForecastChart;