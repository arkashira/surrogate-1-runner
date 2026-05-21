import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api/gpu';

export const getGPUPerformance = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/performance`);
    return response.data;
  } catch (error) {
    console.error('Error fetching GPU performance:', error);
    throw error;
  }
};

export const getFirmwareStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/firmware`);
    return response.data;
  } catch (error) {
    console.error('Error fetching firmware status:', error);
    throw error;
  }
};