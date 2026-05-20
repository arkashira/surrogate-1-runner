import React from 'react';

/**
 * ProviderSelector
 *
 * Renders a dropdown for selecting an LLM provider.
 *
 * Props:
 * - selectedProvider: string | undefined
 *   The currently selected provider value.
 * - onChange: (value: string) => void
 *   Callback invoked when the user selects a different provider.
 *
 * The component is intentionally lightweight and stateless; it
 * delegates state management to the parent wizard component.
 */
const providers = [
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'cohere', label: 'Cohere' },
];

const ProviderSelector = ({ selectedProvider, onChange }) => (
  <div className="provider-selector">
    <label htmlFor="provider-select" className="provider-label">
      Select LLM Provider:
    </label>
    <select
      id="provider-select"
      className="provider-select"
      value={selectedProvider || ''}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="" disabled>
        -- Choose provider --
      </option>
      {providers.map((p) => (
        <option key={p.value} value={p.value}>
          {p.label}
        </option>
      ))}
    </select>
  </div>
);

export default ProviderSelector;