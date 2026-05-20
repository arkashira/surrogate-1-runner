import React, { useState } from 'react';
import { FormControl, InputLabel, Select, MenuItem, Button } from '@material-ui/core';

const CpuSelection = ({ onSelect }) => {
  const [selectedCpu, setSelectedCpu] = useState('');

  const handleChange = (event) => {
    setSelectedCpu(event.target.value);
  };

  const handleSubmit = () => {
    onSelect(selectedCpu);
  };

  return (
    <div>
      <FormControl fullWidth>
        <InputLabel>CPU</InputLabel>
        <Select value={selectedCpu} onChange={handleChange}>
          <MenuItem value="Intel i9-13900K">Intel i9-13900K</MenuItem>
          <MenuItem value="AMD Ryzen 9 7950X">AMD Ryzen 9 7950X</MenuItem>
          {/* Add more CPU options */}
        </Select>
      </FormControl>
      <Button variant="contained" color="primary" onClick={handleSubmit}>
        Select CPU
      </Button>
    </div>
  );
};

export default CpuSelection;