import { CostOptimizationClient } from 'costinel-api';

export class CostOptimizationService {
  private client: CostOptimizationClient;

  constructor() {
    this.client = new CostOptimizationClient();
  }

  async setCostOptimizationPolicy(policy: any): Promise<void> {
    await this.client.setPolicy(policy);
  }

  async enforcePolicies(): Promise<void> {
    await this.client.enforcePolicies(); // Correct method name from Candidate 2
  }

  async reportViolations(): Promise<any[]> {
    return await this.client.reportViolations(); // Correct method name from Candidate 2
  }
}

// Example usage with error handling:
const service = new CostOptimizationService();
const policy = {
  // Define your cost optimization policy here
};

(async () => {
  try {
    await service.setCostOptimizationPolicy(policy);
    await service.enforcePolicies();
    const violations = await service.reportViolations();
    console.log('Policy violations:', violations);
  } catch (error) {
    console.error('Error handling cost optimization:', error);
  }
})();