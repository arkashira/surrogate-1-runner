import React from 'react';
import { Button } from 'antd';

const SuccessMessage = ({ onClose }) => {
  return (
    <div className="success-message">
      <h2>Setup Complete!</h2>
      <p>Your surrogate-1 instance is now ready for data generation.</p>
      <Button type="primary" onClick={onClose}>
        Start Generating Data
      </Button>
    </div>
  );
};

export default SuccessMessage;