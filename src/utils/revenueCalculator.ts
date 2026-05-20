import { Scenario, SimulationResult, ScenarioWithRevenue } from '../types/simulation';

/**
 * Calculate projected revenue for a scenario
 * Revenue = Sum of (price × customers) for all pricing tiers
 */
export function calculateScenarioRevenue(scenario: Scenario): number {
  return scenario.pricingTiers.reduce(
    (total, tier) => total + (tier.price * tier.customers),
    0
  );
}

/**
 * Process scenarios and determine optimal (highest revenue) scenario
 */
export function processScenarios(scenarios: Scenario[]): ScenarioWithRevenue[] {
  const results = scenarios.map((scenario) => ({
    ...scenario,
    projectedRevenue: calculateScenarioRevenue(scenario),
    isOptimal: false,
  }));

  // Find and mark the optimal scenario
  const maxRevenue = Math.max(...results.map((r) => r.projectedRevenue));
  return results.map((r) => ({
    ...r,
    isOptimal: r.projectedRevenue === maxRevenue,
  }));
}

/**
 * Format currency for display
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}