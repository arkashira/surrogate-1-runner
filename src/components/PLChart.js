import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const PLChart = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef && chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      const chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(item => item.date),
          datasets: [
            {
              label: 'Profit & Loss',
              data: data.map(item => item.value),
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `Value: ${context.parsed.y}`;
                },
              },
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Date',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Amount',
              },
            },
          },
        },
      });

      return () => {
        chart.destroy();
      };
    }
  }, [data]);

  return <canvas ref={chartRef} />;
};

export default PLChart;