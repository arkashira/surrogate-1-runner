import axios from 'axios';

export const fetchIntegrationStatus = async () => {
  try {
    const response = await axios.get('/api/integration/status');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch integration status');
  }
};