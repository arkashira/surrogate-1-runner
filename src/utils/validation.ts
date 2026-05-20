export interface PolicyViolation {
  policyName: string;
  resourceType: string;
  violationDetails: Record<string, any>;
  autoRemediated?: boolean;
}

export interface CostPolicy {
  name: string;
  maxInstanceSize?: string;
  idleTimeoutMinutes?: number;
  allowedRegions?: string[];
}

export const validateAgainstPolicies = (
  resourceConfig: Record<string, any>,
  policies: CostPolicy[]
): PolicyViolation[] => {
  const violations: PolicyViolation[] = [];
  
  for (const policy of policies) {
    if (policy.maxInstanceSize && resourceConfig.instanceType) {
      const sizeOrder = ['t2.micro', 't2.small', 't2.medium', 'm5.large', 'm5.xlarge'];
      const configSizeIndex = sizeOrder.indexOf(resourceConfig.instanceType);
      const maxSizeIndex = sizeOrder.indexOf(policy.maxInstanceSize);
      
      if (configSizeIndex > maxSizeIndex) {
        violations.push({
          policyName: policy.name,
          resourceType: resourceConfig.type,
          violationDetails: {
            requestedSize: resourceConfig.instanceType,
            maxSizeAllowed: policy.maxInstanceSize
          },
          autoRemediated: true
        });
        
        // Auto-remediate by adjusting instance size
        resourceConfig.instanceType = policy.maxInstanceSize;
      }
    }
    
    if (policy.idleTimeoutMinutes && resourceConfig.idleTimeout) {
      if (resourceConfig.idleTimeout > policy.idleTimeoutMinutes) {
        violations.push({
          policyName: policy.name,
          resourceType: resourceConfig.type,
          violationDetails: {
            requestedTimeout: resourceConfig.idleTimeout,
            maxTimeoutAllowed: policy.idleTimeoutMinutes
          }
        });
      }
    }
    
    if (policy.allowedRegions && resourceConfig.region) {
      if (!policy.allowedRegions.includes(resourceConfig.region)) {
        violations.push({
          policyName: policy.name,
          resourceType: resourceConfig.type,
          violationDetails: {
            requestedRegion: resourceConfig.region,
            allowedRegions: policy.allowedRegions
          }
        });
      }
    }
  }
  
  return violations;
};