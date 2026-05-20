import React, { useState } from 'react';

const BuildRecommendationForm = () => {
  const [budget, setBudget] = useState(1000);
  const [usageType, setUsageType] = useState('gaming');
  const [components, setComponents] = useState({
    cpu: '',
    gpu: '',
    ram: '',
    storage: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (budget < 200) {
      setError('Budget must be at least $200');
      return;
    }

    // Mock API call - would integrate with recommendation engine
    console.log('Generating recommendation with:', {
      budget,
      usageType,
      components
    });

    setError('');
  };

  return (
    <form onSubmit={handleSubmit} className="build-recommendation-form">
      <div className="form-group">
        <label>
          Budget ($):
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(parseInt(e.target.value))}
            min="200"
            required
          />
        </label>
      </div>

      <div className="form-group">
        <label>
          Primary Usage:
          <select 
            value={usageType}
            onChange={(e) => setUsageType(e.target.value)}
          >
            <option value="gaming">Gaming</option>
            <option value="streaming">Streaming</option>
            <option value="productivity">Productivity</option>
            <option value="content-creation">Content Creation</option>
          </select>
        </label>
      </div>

      <div className="component-preferences">
        <h3>Component Preferences</h3>
        {Object.entries(components).map(([key, value]) => (
          <div key={key} className="form-group">
            <label>
              {key.toUpperCase() + ':'}
              <input
                type="text"
                value={value}
                onChange={(e) => setComponents({
                  ...components,
                  [key]: e.target.value
                })}
                placeholder={`Preferred ${key} (optional)`}
              />
            </label>
          </div>
        ))}
      </div>

      {error && <div className="error-message">{error}</div>}

      <button type="submit" className="submit-button">
        Generate Recommendations
      </button>
    </form>
  );
};

export default BuildRecommendationForm;