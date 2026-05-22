
import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chartjs-library';

ChartJS.register(Line);

const options = {
  responsive: true,
  plugins: {
    title: {
      display: true,
      text: 'Language Learning Progress',
    },
  },
  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'day',
      },
    },
    y: {
      beginAtZero: true,
      max: 100,
    },
  },
};

const data = {
  labels: [],
  datasets: [
    {
      label: 'Progress',
      data: [],
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    },
  ],
};

export function ProgressVisualization({ progressData }) {
  data.labels = progressData.dates;
  data.datasets[0].data = progressData.scores;

  return (
    <div>
      <Line options={options} data={data} />
    </div>
  );
}