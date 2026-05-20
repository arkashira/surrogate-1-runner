import { Policy, Violation } from '../models';
import { CloudProvider } from '../providers';
import { Logger } from '../utils';

export class EnforcementService {
  private logger: Logger;
  private cloudProvider: CloudProvider;

  constructor(logger: Logger, cloudProvider: CloudProvider) {
    this.logger = logger;
    this.cloudProvider = cloudProvider;
  }

  async enforcePolicy(policy: Policy): Promise<Violation[]> {
    this.logger.info(`Enforcing policy: ${policy.id}`);

    const violations: Violation[] = [];

    // Implement policy enforcement logic here based on the provided policy
    // Use the cloudProvider to interact with the cloud infrastructure
    // and check for policy violations

    // Example: Check if the resource usage exceeds the defined limit
    const resources = await this.cloudProvider.getResources();
    if (resources.usage > policy.limit) {
      violations.push({
        id: `${policy.id}-usage-exceed`,
        message: `Resource usage exceeds the defined limit`,
        details: { usage: resources.usage, limit: policy.limit },
      });
    }

    return violations;
  }
}