import React, { useState, useEffect } from 'react';
import { fetchPriceComparison } from '../utils/priceComparison';

const ComponentComparison = ({ componentId }) => {
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadComparisonData = async () => {
      try {
        setLoading(true);
        const data = await fetchPriceComparison(componentId);
        setComparisonData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (componentId) {
      loadComparisonData();
    }
  }, [componentId]);

  if (loading) return <div className="loading">Loading price comparison...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!comparisonData) return <div>No comparison data available</div>;

  return (
    <div className="component-comparison">
      <h2>Price Comparison for {comparisonData.componentName}</h2>
      <div className="comparison-results">
        {comparisonData.retailers.map((retailer) => (
          <div key={retailer.name} className="retailer-card">
            <h3>{retailer.name}</h3>
            <p className="price">${retailer.price.toFixed(2)}</p>
            <p className="availability">{retailer.availability}</p>
            <a href={retailer.url} target="_blank" rel="noopener noreferrer">
              View Product
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ComponentComparison;