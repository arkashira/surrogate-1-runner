import React, { useState, useEffect } from 'react';
import './styles/dashboard.css';

const Dashboard = () => {
  const [timeFrame, setTimeFrame] = useState('30-day');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({ months: [], revenue: [], expenses: [] });

  useEffect(() => {
    const timer = setTimeout(() => {
      // Simulate API call with debounce
      fetchData();
    }, 300);
    return () => clearTimeout(timer);
  }, [timeFrame, startDate, endDate]);

  const fetchData = async () => {
    setLoading(true);
    // In production, this would call an API endpoint
    // Example mock data for 12 months
    const mockMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const mockRevenue = mockMonths.map(() => Math.floor(Math.random() * 50000) + 10000);
    const mockExpenses = mockMonths.map(() => Math.floor(Math.random() * 30000) + 5000);
    
    setData({ months: mockMonths, revenue: mockRevenue, expenses: mockExpenses });
    setLoading(false);
  };

  const handleTimeFrameChange = (e) => {
    const selected = e.target.value;
    setTimeFrame(selected);
    setStartDate('');
    setEndDate('');
  };

  const handleCustomDateChange = (dates) => {
    if (dates.length === 2) {
      setStartDate(dates[0].toISOString().split('T')[0]);
      setEndDate(dates[1].toISOString().split('T')[0]);
    }
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Profit & Loss Dashboard</h1>
      
      <div className="time-filters">
        <select 
          className="time-frame-select"
          value={timeFrame}
          onChange={handleTimeFrameChange}
        >
          <option value="7-day">7-Day</option>
          <option value="30-day">30-Day</option>
          <option value="custom">Custom Range</option>
        </select>
        
        {timeFrame === 'custom' && (
          <div className="date-range-picker">
            <input 
              type="date"
              onChange={(e) => handleCustomDateChange([new Date(e.target.value), new Date(endDate)])}
            />
            <span>to</span>
            <input 
              type="date"
              onChange={(e) => handleCustomDateChange([new Date(startDate), new Date(e.target.value)])}
            />
          </div>
        )}
      </div>

      <div className="chart-container">
        {loading ? (
          <div className="loading-indicator">Loading financial data...</div>
        ) : (
          <LineChart 
            data={data}
            width={800}
            height={400}
          />
        )}
      </div>
    </div>
  );
};

// Placeholder for chart implementation
const LineChart = ({ data, width, height }) => (
  <div className="line-chart" style={{ width, height }}>
    <h3>Monthly Revenue & Expenses</h3>
    <div className="chart-grid">
      {data.months.map((month, i) => (
        <div key={i} className="chart-bar">
          <div className="revenue-bar" style={{ width: `${data.revenue[i]/100}%` }}></div>
          <div className="expense-bar" style={{ width: `${data.expenses[i]/100}%` }}></div>
          <div className="month-label">{month}</div>
        </div>
      ))}
    </div>
  </div>
);

export default Dashboard;