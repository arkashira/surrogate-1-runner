import React, { useEffect, useState } from 'react';
import { fetchComponentBenchmarks } from '../utils/api';

const ComponentDetails = ({ componentId }) => {
  const [benchmarks, setBenchmarks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchComponentBenchmarks(componentId)
      .then(data => {
        setBenchmarks(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [componentId]);

  if (loading) return <div>Loading performance data...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="component-details">
      <h2>Performance Benchmarks</h2>
      <table className="benchmarks-table">
        <thead>
          <tr>
            <th>Test Scenario</th>
            <th>Result</th>
            <th>Units</th>
          </tr>
        </thead>
        <tbody>
          {benchmarks.map((bench, index) => (
            <tr key={index}>
              <td>{bench.test_name}</td>
              <td>{bench.value}</td>
              <td>{bench.unit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ComponentDetails;