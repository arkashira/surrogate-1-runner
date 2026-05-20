import React, { useState } from 'react';

const IdeaInputForm = () => {
  const [idea, setIdea] = useState('');
  const [validationPlan, setValidationPlan] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    // Simulate generating a validation plan based on the input idea
    const generatedPlan = generateValidationPlan(idea);
    setValidationPlan(generatedPlan);
  };

  const generateValidationPlan = (inputIdea) => {
    // Placeholder logic for generating a validation plan
    return {
      steps: [
        { step: 1, description: `Define target market for ${inputIdea}` },
        { step: 2, description: `Conduct initial market research for ${inputIdea}` },
        { step: 3, description: `Create MVP prototype for ${inputIdea}` }
      ],
      successThresholds: [
        { metric: 'User engagement', threshold: '10% increase' },
        { metric: 'Customer acquisition cost', threshold: 'Below $5' }
      ]
    };
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your startup idea:
          <input type="text" value={idea} onChange={(e) => setIdea(e.target.value)} />
        </label>
        <button type="submit">Submit</button>
      </form>
      {validationPlan && (
        <div>
          <h2>Validation Plan:</h2>
          <h3>Steps:</h3>
          <ul>
            {validationPlan.steps.map((step) => (
              <li key={step.step}>{step.description}</li>
            ))}
          </ul>
          <h3>Success Thresholds:</h3>
          <ul>
            {validationPlan.successThresholds.map((threshold) => (
              <li key={threshold.metric}>{`${threshold.metric}: ${threshold.threshold}`}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default IdeaInputForm;