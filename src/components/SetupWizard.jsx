
import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';
import { ModelSelect, DataSizeSelect } from './';

const SetupWizard = () => {
  const [model, setModel] = useState('');
  const [dataSize, setDataSize] = useState(10000);

  const onFinish = (values) => {
    // Handle form submission here
    console.log('Received values:', values);
  };

  return (
    <Form onFinish={onFinish}>
      <ModelSelect value={model} onChange={setModel} />
      <DataSizeSelect value={dataSize} onChange={setDataSize} />
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Confirm
        </Button>
      </Form.Item>
    </Form>
  );
};

export default SetupWizard;

// src/components/ModelSelect.jsx

import React from 'react';

const ModelSelect = ({ value, onChange }) => {
  const options = [
    { label: 'Model 1', value: 'model1' },
    { label: 'Model 2', value: 'model2' },
    // Add more models as needed
  ];

  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default ModelSelect;

// src/components/DataSizeSelect.jsx

import React from 'react';

const DataSizeSelect = ({ value, onChange }) => {
  return (
    <select value={value} onChange={(e) => onChange(parseInt(e.target.value))}>
      {Array.from({ length: 10 }, (_, i) => (
        <option key={i + 1} value={i + 10000}>
          {(i + 1) * 10000}
        </option>
      ))}
    </select>
  );
};

export default DataSizeSelect;