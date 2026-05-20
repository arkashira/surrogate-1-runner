export interface PricingTier {
  tier: string;
  price: number;
  customers: number;
}

export interface Scenario {
  id: string;
  name: string;
  pricingTiers: PricingTier[];
}

export interface SimulationResult {
  scenarioId: string;
  projectedRevenue: number;
}

export interface ScenarioWithRevenue extends Scenario {
  projectedRevenue: number;
  isOptimal: boolean;
}