import React from 'react';

export const Stepper = ({ currentStep, steps, completedSteps = [] }) => {
  return (
    <div className="stepper-container">
      <div className="stepper-track">
        {steps.map((step, index) => {
          const isActive = index === currentStep;
          const isCompleted = completedSteps.includes(step.id) || index < currentStep;
          
          return (
            <div 
              key={step.id} 
              className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
            >
              <div className="step-indicator">
                {isCompleted ? (
                  <span className="check-icon">✓</span>
                ) : (
                  <span className="step-number">{index + 1}</span>
                )}
              </div>
              <div className="step-label">
                <span className="step-title">{step.title}</span>
                {isActive && <span className="step-description">{step.description}</span>}
              </div>
              {index < steps.length - 1 && <div className="step-connector" />}
            </div>
          );
        })}
      </div>
    </div>
  );
};