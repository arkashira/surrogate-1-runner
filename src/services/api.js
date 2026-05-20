import axios from 'axios';

const API_BASE_URL = 'https://api.axentx.com';

export const getInstanceData = async (instanceId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/instances/${instanceId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching instance data:', error);
    throw error;
  }
};