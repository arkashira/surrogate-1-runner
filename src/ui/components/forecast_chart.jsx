import React from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const ForecastChart = () => {
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/forecast');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching forecast data:', error);
      }
    };

    fetchData();
  }, []);

  const chartData = {
    labels: data?.labels || [],
    datasets: [
      {
        label: 'Historical Costs',
        data: data?.historical || [],
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false,
      },
      {
        label: 'Forecasted Costs',
        data: data?.forecast || [],
        borderColor: 'rgba(255, 99, 132, 1)',
        fill: false,
      },
    ],
  };

  return (
    <div>
      <h2>Cloud Cost Forecast</h2>
      {data ? (
        <Line data={chartData} options={{ responsive: true }} />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default ForecastChart;