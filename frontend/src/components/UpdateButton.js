import React, { useState } from 'react';
import axios from 'axios';

const UpdateButton = ({ serviceName }) => {
  const [updateStatus, setUpdateStatus] = useState('idle');

  const handleUpdateClick = async () => {
    setUpdateStatus('updating');
    try {
      const response = await axios.post(`/api/update-service/${serviceName}`);
      if (response.status === 200) {
        setUpdateStatus('success');
      } else {
        setUpdateStatus('error');
      }
    } catch (error) {
      console.error('Error updating service:', error);
      setUpdateStatus('error');
    }
  };

  return (
    <button onClick={handleUpdateClick} disabled={updateStatus === 'updating'}>
      {updateStatus === 'idle' && 'Update'}
      {updateStatus === 'updating' && 'Updating...'}
      {updateStatus === 'success' && 'Updated'}
      {updateStatus === 'error' && 'Error'}
    </button>
  );
};

export default UpdateButton;