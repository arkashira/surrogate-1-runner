export interface CostAnomaly {
  id: string;
  severity: string;
  type: string;
  timestamp: string;
  description: string;
  remediation: string;
}

export interface CostAnomalyFilter {
  severity?: string;
  type?: string;
  timeRange?: string;
}