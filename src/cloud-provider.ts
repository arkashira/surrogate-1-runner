
import { UsageRecord, CostRecord } from './types';

// Abstract base class for individual cloud services (AWS, GCP, Azure)
export abstract class CloudService {
  abstract fetchUsage(): Promise<UsageRecord[]>;
  abstract fetchCosts(): Promise<CostRecord[]>;
}

// Concrete implementations would go here (e.g., class AWSCloudService implements CloudService)

export class CloudProvider {
  private services: CloudService[];

  constructor(services: CloudService[] = []) {
    this.services = services;
  }

  // Register a new cloud service provider
  public addService(service: CloudService): void {
    this.services.push(service);
  }

  public async getAggregatedMetrics(): Promise<{ usage: UsageRecord[], costs: CostRecord[] }> {
    const allUsage: UsageRecord[] = [];
    const allCosts: CostRecord[] = [];

    // Fetch data from all registered services in parallel
    const promises = this.services.map(async (service) => {
      const [usage, costs] = await Promise.all([
        service.fetchUsage(),
        service.fetchCosts()
      ]);
      return { usage, costs };
    });

    const results = await Promise.all(promises);

    results.forEach(result => {
      allUsage.push(...result.usage);
      allCosts.push(...result.costs);
    });

    return { usage: allUsage, costs: allCosts };
  }
}