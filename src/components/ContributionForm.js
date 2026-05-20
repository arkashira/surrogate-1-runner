import React, { useState } from 'react';

const ContributionForm = () => {
  const [contributionDate, setContributionDate] = useState('05');
  const [contributionAmount, setContributionAmount] = useState('');
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    const amountNum = parseFloat(contributionAmount);
    
    if (isNaN(amountNum) || amountNum <= 0) {
      newErrors.amount = 'Amount must be a positive number';
    } else if (amountNum < 1 || amountNum > 10000) {
      newErrors.amount = 'Amount must be between $1 and $10,000';
    }
    
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    
    // Form submission logic here
    console.log({
      contributionDate,
      contributionAmount: parseFloat(contributionAmount)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          Monthly Contribution Date:
          <select 
            value={contributionDate} 
            onChange={(e) => setContributionDate(e.target.value)}
          >
            {[...Array(31)].map((_, i) => (
              <option key={i+1} value={String(i+1).padStart(2, '0')}>
                {i+1}
              </option>
            ))}
          </select>
        </label>
      </div>
      
      <div>
        <label>
          Contribution Amount ($):
          <input
            type="number"
            value={contributionAmount}
            onChange={(e) => setContributionAmount(e.target.value)}
            min="1"
            max="10000"
          />
          {errors.amount && <span style={{ color: 'red' }}>{errors.amount}</span>}
        </label>
      </div>
      
      <button type="submit">Save Contribution Settings</button>
    </form>
  );
};

export default ContributionForm;