import React from 'react';
import { Alert } from 'antd';

interface ErrorHandlingProps {
  error: string;
}

const ErrorHandling: React.FC<ErrorHandlingProps> = ({ error }) => {
  return (
    <Alert
      message="Error"
      description={error}
      type="error"
      showIcon
    />
  );
};

export default ErrorHandling;