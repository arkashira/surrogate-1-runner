import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchOnboardingCompletionData } from '../services/api';

const AnalyticsDashboard = () => {
  const [data, setData] = useState([]);
  const [timePeriod, setTimePeriod] = useState('week');

  useEffect(() => {
    const fetchData = async () => {
      const result = await fetchOnboardingCompletionData(timePeriod);
      setData(result);
    };
    fetchData();
  }, [timePeriod]);

  const handleTimePeriodChange = (event) => {
    setTimePeriod(event.target.value);
  };

  return (
    <div className="analytics-dashboard">
      <h1>Onboarding Completion Rates</h1>
      <div className="time-period-selector">
        <label htmlFor="time-period">Select Time Period:</label>
        <select id="time-period" value={timePeriod} onChange={handleTimePeriodChange}>
          <option value="week">Last Week</option>
          <option value="month">Last Month</option>
          <option value="quarter">Last Quarter</option>
        </select>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="step" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="completionRate" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AnalyticsDashboard;