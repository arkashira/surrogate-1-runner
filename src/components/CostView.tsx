import React, { useState } from 'react';
import ProviderSelector from './ProviderSelector';
import { Typography, Box } from '@mui/material';

const CostView: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState<string>('');

  const handleProviderChange = (provider: string) => {
    setSelectedProvider(provider);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Unified Cost View
      </Typography>
      <ProviderSelector onProviderChange={handleProviderChange} />
      {selectedProvider && (
        <Typography variant="h6" sx={{ mt: 2 }}>
          Showing costs for {selectedProvider.toUpperCase()}
        </Typography>
      )}
    </Box>
  );
};

export default CostView;