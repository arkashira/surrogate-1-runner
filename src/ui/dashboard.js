import React, { useState, useEffect } from 'react';
import { fetchRecommendations } from '../api/recommendations';

const Dashboard = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadRecommendations = async () => {
      try {
        const data = await fetchRecommendations();
        setRecommendations(data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    loadRecommendations();
  }, []);

  return (
    <div className="dashboard">
      <h1>Cloud Infrastructure Dashboard</h1>
      <div className="recommendations-section">
        <h2>Cost Optimization Recommendations</h2>
        {loading ? (
          <p>Loading recommendations...</p>
        ) : (
          <ul>
            {recommendations.map((recommendation, index) => (
              <li key={index}>
                <h3>{recommendation.title}</h3>
                <p>{recommendation.description}</p>
                <button onClick={() => applyRecommendation(recommendation)}>
                  Apply Recommendation
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

const applyRecommendation = (recommendation) => {
  // Implement the logic to apply the recommendation
  console.log(`Applying recommendation: ${recommendation.title}`);
};

export default Dashboard;