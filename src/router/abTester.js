
class ABTester {
  constructor() {
    this.strategies = {
      'costBased': this.costBasedStrategy,
      'random': this.randomStrategy,
    };
    this.metrics = {};
  }

  async runABTest(request, strategyA, strategyB, iterations = 100) {
    const results = {
      [strategyA]: { cost: 0, count: 0 },
      [strategyB]: { cost: 0, count: 0 },
    };

    for (let i = 0; i < iterations; i++) {
      const strategy = Math.random() < 0.5 ? strategyA : strategyB;
      const provider = await this[strategy](request);
      const cost = await this.getProviderCost(provider, request);

      results[strategy].cost += cost;
      results[strategy].count++;
    }

    return results;
  }

  async costBasedStrategy(request) {
    const providers = await getProviders(request);
    const requestType = getRequestType(request);

    // Sort providers by cost for the request type
    providers.sort((a, b) => a.costs[requestType] - b.costs[requestType]);

    return providers[0];
  }

  async randomStrategy(request) {
    const providers = await getProviders(request);
    const randomIndex = Math.floor(Math.random() * providers.length);

    return providers[randomIndex];
  }

  async getProviderCost(provider, request) {
    const requestType = getRequestType(request);
    return provider.costs[requestType];
  }

  async trackMetric(strategy, cost) {
    if (!this.metrics[strategy]) {
      this.metrics[strategy] = { totalCost: 0, count: 0 };
    }

    this.metrics[strategy].totalCost += cost;
    this.metrics[strategy].count++;
  }

  getMetrics() {
    return this.metrics;
  }
}

module.exports = ABTester;