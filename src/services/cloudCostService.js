const axios = require('axios');

class CloudCostService {
  async getCurrentCosts() {
    try {
      const response = await axios.get('https://api.cloudprovider.com/costs');
      return response.data;
    } catch (error) {
      console.error('Error fetching costs from cloud provider:', error);
      throw error;
    }
  }
}

module.exports = new CloudCostService();