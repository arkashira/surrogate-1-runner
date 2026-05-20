const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

class CostinelService {
  constructor(config) {
    this.apiKey = config.apiKey || process.env.COSTINEL_API_KEY;
    this.baseUrl = config.baseUrl || process.env.COSTINEL_BASE_URL || 'https://api.costinel.io/v1';
    this.updateInterval = config.updateInterval || 5 * 60 * 1000; // 5 minutes in ms
    this.cache = new Map();
    this.cacheTimestamp = new Map();
  }

  async fetchCostMetrics(serviceType, timeRange) {
    const cacheKey = `${serviceType}:${timeRange}`;
    const now = Date.now();

    // Check cache first (5 minute TTL)
    if (this.cache.has(cacheKey) && this.cacheTimestamp.get(cacheKey) > now - this.updateInterval) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await axios.get(`${this.baseUrl}/metrics/cost`, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        params: {
          service_type: serviceType,
          time_range: timeRange,
          format: 'json',
        },
        timeout: 10000,
      });

      const data = response.data;
      
      // Cache the result
      this.cache.set(cacheKey, data);
      this.cacheTimestamp.set(cacheKey, now);

      return data;
    } catch (error) {
      console.error('Costinel API error:', error.message);
      
      // Return cached data if available, otherwise throw
      if (this.cache.has(cacheKey)) {
        console.warn('Returning stale cached data');
        return this.cache.get(cacheKey);
      }
      
      throw new Error(`Failed to fetch cost metrics: ${error.message}`);
    }
  }

  async getAllCostMetrics(timeRange) {
    const serviceTypes = ['compute', 'storage', 'network', 'database', 'ml'];
    const allMetrics = {};

    for (const serviceType of serviceTypes) {
      try {
        const metrics = await this.fetchCostMetrics(serviceType, timeRange);
        allMetrics[serviceType] = metrics;
      } catch (error) {
        console.error(`Failed to fetch metrics for ${serviceType}:`, error.message);
        allMetrics[serviceType] = null;
      }
    }

    return allMetrics;
  }

  async getCostSummary(timeRange) {
    const allMetrics = await this.getAllCostMetrics(timeRange);
    
    let totalCost = 0;
    const breakdown = {};

    for (const [serviceType, metrics] of Object.entries(allMetrics)) {
      if (metrics && metrics.total_cost) {
        totalCost += metrics.total_cost;
        breakdown[serviceType] = metrics.total_cost;
      }
    }

    return {
      total_cost: totalCost,
      breakdown: breakdown,
      time_range: timeRange,
      timestamp: new Date().toISOString(),
    };
  }

  async startAutoRefresh(callback) {
    const intervalId = setInterval(async () => {
      try {
        const summary = await this.getCostSummary('24h');
        callback(summary);
      } catch (error) {
        console.error('Auto-refresh failed:', error.message);
      }
    }, this.updateInterval);

    return intervalId;
  }
}

module.exports = CostinelService;