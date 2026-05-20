
export interface UsageRecord {
  resourceId: string;
  resourceName: string;
  usage: number;
  usageUnit: string; // e.g., 'GB-Hours', 'vCPU-Hours'
  timestamp: string; // ISO 8601
}

export interface CostRecord {
  resourceId: string;
  cost: number; // Cost in USD
  timestamp: string; // ISO 8601
}

export interface OptimizationSuggestion {
  title: string;
  description: string;
  estimatedSavings: number; // USD
  resourceId: string;
  action: 'TERMINATE' | 'DOWNSCALE' | 'RESIZE';
}