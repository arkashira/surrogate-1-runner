import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';
import { fetchDailyCosts, fetchBudgetStatus } from './api';

// Configuration constants
const POLL_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes
const DEFAULT_BUDGET = {
  used: 0,
  total: 1000, // Default monthly budget
  threshold: 80 // 80% threshold
};

function Dashboard() {
  const [dailyCosts, setDailyCosts] = useState([]);
  const [budget, setBudget] = useState(DEFAULT_BUDGET);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const pollingRef = useRef(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [costsData, budgetData] = await Promise.all([
        fetchDailyCosts(),
        fetchBudgetStatus()
      ]);

      // Filter costs to current month
      const now = new Date();
      const currentMonthCosts = costsData.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate.getMonth() === now.getMonth() &&
               itemDate.getFullYear() === now.getFullYear();
      });

      setDailyCosts(currentMonthCosts);
      setBudget(budgetData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    loadData();

    // Set up polling
    pollingRef.current = setInterval(loadData, POLL_INTERVAL_MS);

    // Cleanup
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, []);

  const budgetPercentage = budget.total > 0
    ? Math.min((budget.used / budget.total) * 100, 100)
    : 0;

  const isOverThreshold = budgetPercentage >= budget.threshold;

  if (loading && dailyCosts.length === 0) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-error">Error: {error}</div>;
  }

  return (
    <div className="dashboard">
      <h1>Cost Dashboard</h1>

      <section className="cost-chart">
        <h2>Daily Costs - Current Month</h2>
        {dailyCosts.length > 0 ? (
          <LineChart
            width={600}
            height={300}
            data={dailyCosts}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="cost" stroke="#3b82f6" />
          </LineChart>
        ) : (
          <div className="chart-empty">No cost data available for current month</div>
        )}
      </section>

      <section className="budget-status">
        <h2>Budget Usage</h2>
        <div className="budget-progress-container">
          <div className={`budget-progress ${isOverThreshold ? 'over-threshold' : ''}`}
               style={{ width: `${budgetPercentage}%` }} />
          <div className="budget-threshold"
               style={{ left: `${budget.threshold}%` }}
               title={`Threshold: ${budget.threshold}%`} />
        </div>
        <div className="budget-details">
          <span>Used: ${budget.used.toFixed(2)}</span>
          <span>Total: ${budget.total.toFixed(2)}</span>
          <span>{budgetPercentage.toFixed(1)}%</span>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;