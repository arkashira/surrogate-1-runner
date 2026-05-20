const axios = require('axios');

class ApiClient {
  constructor(baseUrl, token) {
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 10000, // Prevent hanging requests
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async get(endpoint, params = {}) {
    try {
      const response = await this.client.get(endpoint, { params });
      return response.data;
    } catch (err) {
      console.error(`API GET ${endpoint} error:`, err.message);
      throw err;
    }
  }

  async post(endpoint, body = {}) {
    try {
      const response = await this.client.post(endpoint, body);
      return response.data;
    } catch (err) {
      console.error(`API POST ${endpoint} error:`, err.message);
      throw err;
    }
  }
}

module.exports = ApiClient;