import React, { useState, useEffect } from 'react';

const ParametersForm = ({ onSubmit, initialParams = {} }) => {
  const [temperature, setTemperature] = useState(initialParams.temperature || 1.0);
  const [topP, setTopP] = useState(initialParams.topP || 1.0);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate inputs
  useEffect(() => {
    const newErrors = {};
    
    if (temperature < 0 || temperature > 2) {
      newErrors.temperature = 'Temperature must be between 0 and 2';
    }
    
    if (topP < 0 || topP > 1) {
      newErrors.topP = 'Top P must be between 0 and 1';
    }
    
    setErrors(newErrors);
  }, [temperature, topP]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (Object.keys(errors).length === 0) {
      setIsSubmitting(true);
      onSubmit({
        temperature: parseFloat(temperature),
        topP: parseFloat(topP)
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="parameter-form">
      <div className="form-group">
        <label htmlFor="temperature">
          Temperature: {temperature}
          <span className="tooltip">ⓘ</span>
          <span className="tooltip-text">
            Controls randomness. Lower values make outputs more focused and deterministic.
          </span>
        </label>
        <input
          type="range"
          id="temperature"
          min="0"
          max="2"
          step="0.1"
          value={temperature}
          onChange={(e) => setTemperature(e.target.value)}
          disabled={isSubmitting}
        />
        <div className="slider-info">
          <span>0 (focused)</span>
          <span>2 (creative)</span>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="topP">
          Top P: {topP}
          <span className="tooltip">ⓘ</span>
          <span className="tooltip-text">
            Controls diversity via nucleus sampling. Lower values limit choices to high-probability tokens.
          </span>
        </label>
        <input
          type="number"
          id="topP"
          min="0"
          max="1"
          step="0.01"
          value={topP}
          onChange={(e) => setTopP(e.target.value)}
          disabled={isSubmitting}
        />
        <div className="slider-info">
          <span>0 (strict)</span>
          <span>1 (diverse)</span>
        </div>
      </div>

      {Object.keys(errors).length > 0 && (
        <div className="error-messages">
          {Object.values(errors).map((error, index) => (
            <div key={index} className="error-message">{error}</div>
          ))}
        </div>
      )}

      <button 
        type="submit" 
        disabled={isSubmitting || Object.keys(errors).length > 0}
        className="submit-button"
      >
        {isSubmitting ? 'Saving...' : 'Save Parameters'}
      </button>
    </form>
  );
};

export default ParametersForm;