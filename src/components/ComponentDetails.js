import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchComponentDetails } from '../utils/api';

const ComponentDetails = () => {
  const { id } = useParams();
  const [component, setComponent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchComponentDetails(id);
        setComponent(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>{component.name}</h1>
      <p><strong>Description:</strong> {component.description}</p>
      <p><strong>Performance Benchmarks:</strong></p>
      <ul>
        {component.performanceBenchmarks.map((benchmark, index) => (
          <li key={index}>{benchmark}</li>
        ))}
      </ul>
    </div>
  );
};

export default ComponentDetails;