import React from 'react';
import ReactDOM from 'react-dom';

function OnboardingUI() {
  return (
    <div>
      <h1>Surrogate-1 Onboarding</h1>
      <p>Welcome to the Surrogate-1 framework onboarding process.</p>
      <button>Get Started</button>
    </div>
  );
}

ReactDOM.render(<OnboardingUI />, document.getElementById('root'));