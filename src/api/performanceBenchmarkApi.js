const axios = require('axios');

const API_BASE_URL = 'https://api.axentx.com/benchmarks';

const fetchPerformanceBenchmarks = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/latest`);
    return response.data;
  } catch (error) {
    console.error('Error fetching performance benchmarks:', error);
    throw error;
  }
};

const updatePerformanceBenchmarks = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/update`);
    return response.data;
  } catch (error) {
    console.error('Error updating performance benchmarks:', error);
    throw error;
  }
};

module.exports = {
  fetchPerformanceBenchmarks,
  updatePerformanceBenchmarks,
};