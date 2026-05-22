import React, { useState, useEffect } from 'react';

const MODEL_OPTIONS = [
  { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', provider: 'OpenAI', description: 'Fast and cost-effective for general tasks' },
  { id: 'gpt-4', name: 'GPT-4', provider: 'OpenAI', description: 'Advanced reasoning and complex tasks' },
  { id: 'claude-3-opus', name: 'Claude 3 Opus', provider: 'Anthropic', description: 'Best for complex reasoning and analysis' },
  { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet', provider: 'Anthropic', description: 'Balanced performance and speed' },
  { id: 'claude-3-haiku', name: 'Claude 3 Haiku', provider: 'Anthropic', description: 'Fastest and most cost-effective Claude' },
  { id: 'command-r', name: 'Command R', provider: 'Cohere', description: 'Optimized for RAG and enterprise use' },
  { id: 'command-light', name: 'Command Light', provider: 'Cohere', description: 'Lightweight and fast for simple tasks' },
];

const ModelSelector = ({ selectedModel, onSelectModel, onNext, onBack, isLastStep }) => {
  const [selected, setSelected] = useState(selectedModel || MODEL_OPTIONS[0]);

  useEffect(() => {
    if (selectedModel) {
      setSelected(selectedModel);
    }
  }, [selectedModel]);

  const handleSelect = (model) => {
    setSelected(model);
    onSelectModel(model);
  };

  return (
    <div className="model-selector-container">
      <h2>Select Your Model</h2>
      <p className="model-description">Choose the AI model you want to use for your surrogate tasks.</p>
      
      <div className="model-grid">
        {MODEL_OPTIONS.map((model) => (
          <div
            key={model.id}
            className={`model-card ${selected.id === model.id ? 'selected' : ''}`}
            onClick={() => handleSelect(model)}
          >
            <div className="model-header">
              <h3>{model.name}</h3>
              <span className="provider-badge">{model.provider}</span>
            </div>
            <p className="model-description">{model.description}</p>
            {selected.id === model.id && (
              <div className="selection-indicator">✓ Selected</div>
            )}
          </div>
        ))}
      </div>

      <div className="model-summary">
        <h4>Selected Model</h4>
        <p><strong>Name:</strong> {selected.name}</p>
        <p><strong>Provider:</strong> {selected.provider}</p>
        <p><strong>Description:</strong> {selected.description}</p>
      </div>

      <div className="wizard-navigation">
        <button
          className="btn btn-secondary"
          onClick={onBack}
          disabled={!isLastStep}
        >
          Back
        </button>
        <button
          className="btn btn-primary"
          onClick={onNext}
          disabled={!selected.id}
        >
          {isLastStep ? 'Start Using' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default ModelSelector;