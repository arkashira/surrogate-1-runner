import React, { useState } from 'react';
import { FormControl, InputLabel, Select, MenuItem, Button } from '@material-ui/core';

const GpuSelection = ({ onSelect }) => {
  const [selectedGpu, setSelectedGpu] = useState('');

  const handleChange = (event) => {
    setSelectedGpu(event.target.value);
  };

  const handleSubmit = () => {
    onSelect(selectedGpu);
  };

  return (
    <div>
      <FormControl fullWidth>
        <InputLabel>GPU</InputLabel>
        <Select value={selectedGpu} onChange={handleChange}>
          <MenuItem value="NVIDIA RTX 4090">NVIDIA RTX 4090</MenuItem>
          <MenuItem value="AMD Radeon RX 7900 XTX">AMD Radeon RX 7900 XTX</MenuItem>
          {/* Add more GPU options */}
        </Select>
      </FormControl>
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        Select GPU
      </Button>
    </div>
  );
};

export default GpuSelection;