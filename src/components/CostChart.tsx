import React from 'react';
import { Line } from 'react-chartjs-2';

interface CostChartProps {
  data: any[];
}

const CostChart: React.FC<CostChartProps> = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: 'Cost',
        data: data.map(item => item.cost),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return <Line data={chartData} />;
};

export default CostChart;