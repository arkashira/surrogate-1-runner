import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import onboardingSteps from '../data/onboardingSteps.json';

const OnboardingWalkthrough = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const navigate = useNavigate();
  const steps = onboardingSteps;

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleLaunch = () => {
    navigate('/labs/aws-first-step');
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2>{steps[currentStep].title}</h2>
        <div style={styles.progress}>
          {steps.map((_, index) => (
            <div 
              key={index} 
              style={{ 
                ...styles.progressDot, 
                backgroundColor: currentStep >= index ? '#4CAF50' : '#ccc' 
              }} 
            />
          ))}
        </div>
      </div>
      <div style={styles.content}>
        <p>{steps[currentStep].description}</p>
        {steps[currentStep].labExplanation && (
          <div style={styles.labExplanation}>
            <h4>Lab Explanation</h4>
            <p>{steps[currentStep].labExplanation}</p>
          </div>
        )}
      </div>
      <div style={styles.actions}>
        {currentStep < steps.length - 1 ? (
          <button onClick={handleNext} style={styles.button}>
            Next Step
          </button>
        ) : (
          <button onClick={handleLaunch} style={styles.button}>
            Launch First Lab
          </button>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: { maxWidth: '600px', margin: '2rem auto', padding: '1.5rem', border: '1px solid #ddd', borderRadius: '8px' },
  header: { marginBottom: '1.5rem' },
  progress: { display: 'flex', gap: '8px', marginTop: '0.5rem' },
  progressDot: { width: '10px', height: '10px', borderRadius: '50%' },
  content: { marginBottom: '2rem' },
  labExplanation: { marginTop: '1rem', padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '4px' },
  actions: { textAlign: 'right' },
  button: { padding: '0.6rem 1.2rem', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }
};

export default OnboardingWalkthrough;