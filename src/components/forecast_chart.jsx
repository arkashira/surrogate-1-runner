import React from 'react';
import { Line } from 'react-chartjs-2';

const ForecastChart = ({ forecastData, actualData }) => {
  const data = {
    labels: forecastData.map(item => item.date),
    datasets: [
      {
        label: 'Forecasted Costs',
        data: forecastData.map(item => item.cost),
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false,
      },
      {
        label: 'Actual Costs',
        data: actualData.map(item => item.cost),
        borderColor: 'rgba(255, 99, 132, 1)',
        fill: false,
      },
    ],
  };

  return (
    <div>
      <Line data={data} options={{ responsive: true }} />
    </div>
  );
};

export default ForecastChart;