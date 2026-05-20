import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setProvider } from '../redux/actions/providerActions';
import { RootState } from '../redux/reducers';

const ProviderSelector: React.FC = () => {
  const dispatch = useDispatch();
  const currentProvider = useSelector((state: RootState) => state.provider.currentProvider);
  const [selectedProvider, setSelectedProvider] = useState(currentProvider);

  useEffect(() => {
    setSelectedProvider(currentProvider);
  }, [currentProvider]);

  const handleProviderChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newProvider = event.target.value;
    setSelectedProvider(newProvider);
    dispatch(setProvider(newProvider));
  };

  return (
    <div className="provider-selector">
      <label htmlFor="provider-select">Select LLM Provider:</label>
      <select
        id="provider-select"
        value={selectedProvider}
        onChange={handleProviderChange}
      >
        <option value="openai">OpenAI</option>
        <option value="anthropic">Anthropic</option>
        <option value="custom">Custom API</option>
      </select>
    </div>
  );
};

export default ProviderSelector;