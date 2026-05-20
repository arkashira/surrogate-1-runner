import React, { useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

const ProfitLossChart = ({ dataSource }) => {
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Revenue',
        data: [],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Expenses',
        data: [],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  });

  useEffect(() => {
    // Simulate fetching data based on the selected data source
    const fetchData = async () => {
      const response = await fetch(`/api/profit-loss?source=${dataSource}`);
      const result = await response.json();
      setData(result);
    };

    fetchData();
  }, [dataSource]);

  return (
    <div>
      <h2>7-Day Revenue/Expense Trends</h2>
      <Line data={data} options={{ responsive: true }} />
      <h2>Current Month-to-Date P&L Summary</h2>
      <Bar data={data} options={{ responsive: true }} />
    </div>
  );
};

export default ProfitLossChart;