import React, { useState } from 'react';
import '../styles/budget.css';

const BudgetForm = ({ onSubmit }) => {
  const [budget, setBudget] = useState('');
  const [confidenceLevel, setConfidenceLevel] = useState('95');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ budget, confidenceLevel });
  };

  return (
    <form onSubmit={handleSubmit} className="budget-form">
      <div className="form-group">
        <label htmlFor="budget">Budget Limit:</label>
        <input
          type="number"
          id="budget"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
          placeholder="Enter budget limit"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="confidenceLevel">Confidence Level:</label>
        <select
          id="confidenceLevel"
          value={confidenceLevel}
          onChange={(e) => setConfidenceLevel(e.target.value)}
        >
          <option value="95">95%</option>
          <option value="90">90%</option>
          <option value="85">85%</option>
        </select>
      </div>
      <button type="submit" className="submit-button">Set Budget</button>
    </form>
  );
};

export default BudgetForm;