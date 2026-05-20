const axios = require('axios');

const API_BASE_URL = 'http://localhost:3001/api';

const api = {
  async getRecordings() {
    try {
      const response = await axios.get(`${API_BASE_URL}/recordings`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recordings:', error);
      throw error;
    }
  },
  // Other API methods...
};

module.exports = api;