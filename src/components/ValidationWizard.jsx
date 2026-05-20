import React, { useState } from 'react';

const steps = [
  { id: 'hypothesis', label: 'Hypothesis' },
  { id: 'metrics', label: 'Metrics' },
  { id: 'thresholds', label: 'Thresholds' },
  { id: 'benchmarks', label: 'Benchmarks' },
];

const ValidationWizard = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    hypothesis: '',
    metrics: '',
    thresholds: '',
    benchmarks: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSave = () => {
    localStorage.setItem('validationWizardData', JSON.stringify(formData));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log('Form submitted:', formData);
  };

  return (
    <div>
      <h2>{steps[currentStep].label}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name={steps[currentStep].id}
          value={formData[steps[currentStep].id]}
          onChange={handleChange}
          required
        />
        <div>
          <button type="button" onClick={handleBack} disabled={currentStep === 0}>
            Back
          </button>
          <button type="button" onClick={handleNext} disabled={currentStep === steps.length - 1}>
            Next
          </button>
          <button type="button" onClick={handleSave}>
            Save Progress
          </button>
          {currentStep === steps.length - 1 && <button type="submit">Finish</button>}
        </div>
      </form>
      {currentStep === steps.length - 1 && (
        <div>
          <h3>Summary</h3>
          <pre>{JSON.stringify(formData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ValidationWizard;