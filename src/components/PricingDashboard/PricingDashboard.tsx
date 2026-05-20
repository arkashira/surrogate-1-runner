import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from 'recharts';
import { usePricingData } from '../../hooks/usePricingData';
import styles from './PricingDashboard.module.css';

const getRandomColor = () =>
  `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;

const PricingDashboard: React.FC = () => {
  const { data, isLoading, isError, error } = usePricingData();

  if (isLoading) return <div className={styles.message}>Loading…</div>;
  if (isError) return <div className={styles.message}>Error: {error.message}</div>;

  // Derive unique categories & competitors
  const categories = Array.from(new Set(data.map((d) => d.category)));
  const competitors = Array.from(new Set(data.map((d) => d.competitor)));

  return (
    <div className={styles.dashboard}>
      <h1>Pricing Analysis Dashboard</h1>

      <div className={styles.charts}>
        {/* Price Trends by Category */}
        <div className={styles.chart}>
          <h2>Price Trends by Product Category</h2>
          <LineChart
            width={800}
            height={400}
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={(d) => new Date(d).toLocaleDateString()} />
            <YAxis />
            <Tooltip />
            <Legend />
            {categories.map((cat) => (
              <Line
                key={cat}
                type="monotone"
                dataKey="price"
                name={cat}
                stroke={getRandomColor()}
                dot={false}
                data={data.filter((item) => item.category === cat)}
              />
            ))}
          </LineChart>
        </div>

        {/* Competitor Comparison */}
        <div className={styles.chart}>
          <h2>Competitor Price Comparison</h2>
          <BarChart
            width={800}
            height={400}
            data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="product" />
            <YAxis />
            <Tooltip />
            <Legend />
            {competitors.map((comp) => (
              <Bar
                key={comp}
                dataKey="price"
                name={comp}
                fill={getRandomColor()}
                data={data.filter((item) => item.competitor === comp)}
              />
            ))}
          </BarChart>
        </div>
      </div>
    </div>
  );
};

export default PricingDashboard;