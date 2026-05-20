const CloudProviderAPI = require('./cloud-providers');

class CloudDashboardAPI {
  constructor() {
    this.providers = ['aws', 'azure', 'gcp'];
    this.costs = {};
  }

  async fetchCosts() {
    for (const provider of this.providers) {
      const api = new CloudProviderAPI(provider);
      this.costs[provider] = await api.getCosts();
    }
  }

  getCosts() {
    return this.costs;
  }
}

module.exports = CloudDashboardAPI;