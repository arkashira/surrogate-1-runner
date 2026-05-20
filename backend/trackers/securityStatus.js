const axios = require('axios');

class SecurityStatus {
  constructor() {
    this.status = 'unknown';
  }

  async fetch() {
    try {
      const response = await axios.get('https://api.example.com/security/status');
      this.status = response.data.status;
    } catch (error) {
      console.error('Error fetching security status:', error);
      this.status = 'error';
    }
  }

  getStatus() {
    return this.status;
  }
}

module.exports = SecurityStatus;