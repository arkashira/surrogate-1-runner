import React, { useState, useEffect } from 'react';
import getBuildRecommendations from '../utils/buildRecommendations';

const ComponentComparison = () => {
  const [userBudget, setUserBudget] = useState(1000);
  const [userNeeds, setUserNeeds] = useState('gaming');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchRecommendations = async () => {
      setLoading(true);
      try {
        const recs = getBuildRecommendations(userBudget, userNeeds);
        setRecommendations(recs);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [userBudget, userNeeds]);

  const handleBudgetChange = (e) => {
    setUserBudget(Number(e.target.value));
  };

  const handleNeedsChange = (e) => {
    setUserNeeds(e.target.value);
  };

  return (
    <div className="component-comparison">
      <h1>PC Build Recommendations</h1>
      
      <div className="user-inputs">
        <div className="input-group">
          <label htmlFor="budget">Budget ($):</label>
          <input
            type="range"
            id="budget"
            min="500"
            max="3000"
            value={userBudget}
            onChange={handleBudgetChange}
          />
          <span>{userBudget}</span>
        </div>
        
        <div className="input-group">
          <label htmlFor="needs">Primary Use:</label>
          <select id="needs" value={userNeeds} onChange={handleNeedsChange}>
            <option value="gaming">Gaming</option>
            <option value="productivity">Productivity</option>
            <option value="content-creation">Content Creation</option>
            <option value="general">General Use</option>
          </select>
        </div>
      </div>

      <div className="recommendations-section">
        <h2>Recommended Builds</h2>
        
        {loading ? (
          <div className="loading">Generating recommendations...</div>
        ) : (
          <div className="recommendations-grid">
            {recommendations.length > 0 ? (
              recommendations.map(build => (
                <div key={build.id} className="build-card">
                  <h3>{build.name}</h3>
                  <div className="build-specs">
                    <p><strong>CPU:</strong> {build.cpu}</p>
                    <p><strong>GPU:</strong> {build.gpu}</p>
                    <p><strong>Motherboard:</strong> {build.motherboard}</p>
                    <p><strong>RAM:</strong> {build.ram}</p>
                    <p><strong>PSU:</strong> {build.psu}</p>
                    <p><strong>SSD:</strong> {build.ssd}</p>
                  </div>
                  <div className="build-footer">
                    <span className="total-cost">${build.totalCost}</span>
                    <span className="relevance">Relevance: {Math.round(build.relevance * 100)}%</span>
                    <span className="value">Value Score: {build.valueScore}/10</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-recommendations">
                No builds found within your budget. Try increasing your budget.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ComponentComparison;