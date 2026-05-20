import React, { useState } from 'react';
import axios from 'axios';
import './SetupWizard.css';

const SetupWizard = ({ onComplete, onSkip }) => {
  const [step, setStep] = useState(1);
  const [apiKey, setApiKey] = useState('');
  const [outputFolder, setOutputFolder] = useState('./output');
  const [touched, setTouched] = useState({ apiKey: false, outputFolder: false });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const isApiKeyValid = apiKey.trim().length > 0;
  const isOutputFolderValid = outputFolder.trim().length > 0;

  const handleApiKeyChange = (event) => {
    setApiKey(event.target.value);
  };

  const handleOutputFolderChange = (event) => {
    setOutputFolder(event.target.value);
  };

  const handleNext = () => {
    if (step === 1 && isApiKeyValid) setStep(2);
  };

  const handleBack = () => {
    if (step === 2) setStep(1);
  };

  const handleSubmit = async () => {
    if (isApiKeyValid && isOutputFolderValid) {
      try {
        const response = await axios.post('/api/setup', {
          apiKey: apiKey.trim(),
          outputFolder: outputFolder.trim(),
        });
        setSuccess(true);
        if (onComplete) onComplete({ apiKey: apiKey.trim(), outputFolder: outputFolder.trim() });
      } catch (error) {
        setError(error.message);
      }
    }
  };

  const handleSkip = () => {
    if (onSkip) onSkip();
  };

  return (
    <div className="setup-wizard-overlay">
      <div className="setup-wizard-modal">
        <h2 className="setup-wizard-title">Setup Wizard</h2>

        {step === 1 && (
          <div className="setup-wizard-step">
            <label htmlFor="api-key">API Key:</label>
            <input
              id="api-key"
              type="text"
              value={apiKey}
              onChange={handleApiKeyChange}
              onBlur={() => setTouched((t) => ({ ...t, apiKey: true }))}
            />
            {touched.apiKey && !isApiKeyValid && <div className="error">API key cannot be empty.</div>}
            <div className="wizard-navigation">
              <button className="wizard-skip" onClick={handleSkip}>Skip</button>
              <button className="wizard-next" onClick={handleNext} disabled={!isApiKeyValid}>Next</button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="setup-wizard-step">
            <label htmlFor="output-folder">Output Folder:</label>
            <input
              id="output-folder"
              type="text"
              value={outputFolder}
              onChange={handleOutputFolderChange}
              onBlur={() => setTouched((t) => ({ ...t, outputFolder: true }))}
            />
            {touched.outputFolder && !isOutputFolderValid && <div className="error">Output folder cannot be empty.</div>}
            <div className="wizard-navigation">
              <button className="wizard-back" onClick={handleBack}>Back</button>
              <button className="wizard-skip" onClick={handleSkip}>Skip</button>
              <button className="wizard-start" onClick={handleSubmit} disabled={!isOutputFolderValid}>Start Generating</button>
            </div>
          </div>
        )}

        {error && <p className="error">{error}</p>}
        {success && <p>Setup complete! Redirecting to main content interface.</p>}
      </div>
    </div>
  );
};

export default SetupWizard;