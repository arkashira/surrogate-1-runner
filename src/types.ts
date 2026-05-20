
export interface Instance {
  id: string;
  instanceType: string;
  utilization: number; // e.g., percentage
  cost: number;
  performance: number;
}

export interface AlternativeInstance {
  id: string;
  instanceType: string;
  cost: number;
  performance: number;
  tradeoff: string; // Description of pros/cons
}

export interface UtilizationMap {
  [instanceId: string]: Instance;
}