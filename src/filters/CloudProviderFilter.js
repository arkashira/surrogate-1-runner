class CloudProviderFilter {
  constructor(data) {
    this.data = data;
    this.providers = ['AWS', 'GCP', 'Azure'];
  }

  applyFilter(provider) {
    if (!this.providers.includes(provider)) {
      throw new Error('Invalid cloud provider');
    }
    return this.data.filter(item => item.provider === provider);
  }

  getProviders() {
    return this.providers;
  }
}

module.exports = CloudProviderFilter;