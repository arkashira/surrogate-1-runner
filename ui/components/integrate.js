import React, { useState } from 'react';
import './integrate.css';

const Integrate = () => {
  const [providers, setProviders] = useState([
    { name: 'Provider A', apiKey: '', isActive: false },
    { name: 'Provider B', apiKey: '', isActive: false },
  ]);
  const [performanceImprovement, setPerformanceImprovement] = useState(null);

  const handleApiKeyChange = (index, value) => {
    const updatedProviders = [...providers];
    updatedProviders[index].apiKey = value;
    setProviders(updatedProviders);
  };

  const handleToggleActive = (index) => {
    const updatedProviders = [...providers];
    updatedProviders[index].isActive = !updatedProviders[index].isActive;
    setProviders(updatedProviders);
  };

  const handleIntegrate = () => {
    // Simulate integration process
    setTimeout(() => {
      setPerformanceImprovement(Math.floor(Math.random() * 30) + 20);
    }, 600000); // Simulate 10 minutes integration process
  };

  return (
    <div className="integrate-container">
      <h2>Integrate LLM Providers</h2>
      <div className="provider-list">
        {providers.map((provider, index) => (
          <div key={index} className="provider-item">
            <h3>{provider.name}</h3>
            <input
              type="text"
              placeholder="API Key"
              value={provider.apiKey}
              onChange={(e) => handleApiKeyChange(index, e.target.value)}
            />
            <button onClick={() => handleToggleActive(index)}>
              {provider.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </div>
        ))}
      </div>
      <button onClick={handleIntegrate} className="integrate-button">
        Integrate Providers
      </button>
      {performanceImprovement && (
        <div className="performance-improvement">
          Performance improved by {performanceImprovement}%
        </div>
      )}
    </div>
  );
};

export default Integrate;