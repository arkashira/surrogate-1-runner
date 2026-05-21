import axios from 'axios';

export const getDataGenerationStatus = async () => {
  try {
    const response = await axios.get('/api/data-generation-status');
    return response.data;
  } catch (error) {
    throw error;
  }
};