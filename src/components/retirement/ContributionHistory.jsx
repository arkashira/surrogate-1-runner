import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ContributionHistory = () => {
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(1);
  const [historicalData, setHistoricalData] = useState([]);
  const [projectedBalance, setProjectedBalance] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchContributionsHistory();
  }, [year, month]);

  const fetchContributionsHistory = async () => {
    setLoading(true);
    try {
      const response = await contributionsService.getContributionsHistory(year, month);
      setHistoricalData(response.data);
      calculateProjectedBalance(response.data);
    } catch (error) {
      console.error('Failed to fetch contributions history:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProjectedBalance = (data) => {
    const currentContributions = data.reduce((sum, item) => sum + item.amount, 0);
    const averageReturnRate = 0.07; // 7% annual return
    const years = 30; // retirement horizon
    const projected = currentContributions * Math.pow(1 + averageReturnRate, years);
    setProjectedBalance(projected.toFixed(2));
  };

  const handleYearChange = (e) => {
    setYear(parseInt(e.target.value));
  };

  const handleMonthChange = (e) => {
    setMonth(parseInt(e.target.value));
  };

  return (
    <div className="contribution-history">
      <h2>Contribution History</h2>
      <div className="filters">
        <label>Year:</label>
        <select value={year} onChange={handleYearChange}>
          {[...Array(11)].map((_, i) => (
            <option key={i} value={new Date().getFullYear() - i}>{new Date().getFullYear() - i}</option>
          ))}
        </select>
        <label>Month:</label>
        <select value={month} onChange={handleMonthChange}>
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>
      {loading ? (
        <p>Loading data...</p>
      ) : (
        <>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="amount" stroke="#8884d8" name="Contribution" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="balance-container">
            <h3>Projected Retirement Balance</h3>
            <p>${projectedBalance}</p>
          </div>
        </>
      )}
    </div>
  );
};

export default ContributionHistory;