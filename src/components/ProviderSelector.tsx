import React, { useState } from 'react';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';

interface ProviderSelectorProps {
  onProviderChange: (provider: string) => void;
}

const ProviderSelector: React.FC<ProviderSelectorProps> = ({ onProviderChange }) => {
  const [selectedProvider, setSelectedProvider] = useState<string>('');

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    const provider = event.target.value as string;
    setSelectedProvider(provider);
    onProviderChange(provider);
  };

  return (
    <FormControl fullWidth>
      <InputLabel id="provider-selector-label">Cloud Provider</InputLabel>
      <Select
        labelId="provider-selector-label"
        id="provider-selector"
        value={selectedProvider}
        onChange={handleChange}
      >
        <MenuItem value="aws">AWS</MenuItem>
        <MenuItem value="gcp">GCP</MenuItem>
        <MenuItem value="azure">Azure</MenuItem>
      </Select>
    </FormControl>
  );
};

export default ProviderSelector;