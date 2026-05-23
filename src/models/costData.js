/**
 * A lightweight immutable representation of the cost data returned by the
 * external API.  It validates the shape of the incoming JSON and exposes
 * helper methods that are useful for dashboards, reports, etc.
 */

class CostData {
  /**
   * @param {Object} params
   * @param {Object<string, {regions: Object<string, number>, total: number}>} params.services
   * @param {Date} [params.timestamp]
   */
  constructor({ services, timestamp = new Date() }) {
    this.services = services;
    this.timestamp = timestamp;
  }

  /**
   * Factory that converts the raw API response into a CostData instance.
   * The API is expected to return:
   * {
   *   services: [
   *     { name: 'Compute', regions: [{ name: 'us-east-1', cost: 120.5 }, …] },
   *     …
   *   ],
   *   timestamp: '2026-05-16T12:00:00Z'   // optional
   * }
   *
   * @param {Object} apiResp
   * @returns {CostData}
   */
  static fromApiResponse(apiResp) {
    if (!apiResp || !Array.isArray(apiResp.services)) {
      throw new Error('Invalid API response: missing services array');
    }

    const services = {};
    for (const svc of apiResp.services) {
      if (!svc.name || !Array.isArray(svc.regions)) {
        continue; // skip malformed entries
      }

      const regionMap = {};
      let total = 0;
      for (const reg of svc.regions) {
        if (typeof reg.name !== 'string' || typeof reg.cost !== 'number') {
          continue;
        }
        regionMap[reg.name] = reg.cost;
        total += reg.cost;
      }

      services[svc.name] = { regions: regionMap, total };
    }

    const timestamp = apiResp.timestamp
      ? new Date(apiResp.timestamp)
      : new Date();

    return new CostData({ services, timestamp });
  }

  /** Total cost across all services */
  getTotalCost() {
    return Object.values(this.services).reduce((sum, svc) => sum + svc.total, 0);
  }

  /** Cost for a specific service and region */
  getCost(serviceName, regionName) {
    const svc = this.services[serviceName];
    if (!svc) return 0;
    return svc.regions[regionName] ?? 0;
  }
}

module.exports = { CostData };