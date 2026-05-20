import { ResourceUsage } from '../types';

export interface CloudProvider {
  getResources(): Promise<ResourceUsage>;
  // Add other cloud provider methods as needed
}

export class AWSCloudProvider implements CloudProvider {
  async getResources(): Promise<ResourceUsage> {
    // Implement logic to fetch resource usage from AWS
    // Return the resource usage as a ResourceUsage object
    // Example:
    // return { usage: 50, limit: 100 };
  }
}