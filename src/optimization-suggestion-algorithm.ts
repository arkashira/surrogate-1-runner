import { CostExplorerClient, GetCostAndUsageCommand } from "@aws-sdk/client-cost-explorer";
import { AWS } from 'aws-sdk';

// ... (existing interfaces and constants)

/**
 * Fetches cost and usage data from AWS Cost Explorer for the last 30 days.
 *
 * @param client Optional CostExplorerClient instance for dependency injection.
 * @returns Promise resolving to an array of ResourceUsage objects.
 */
export async function fetchCostData(
  client: CostExplorerClient = new CostExplorerClient({})
): Promise<ResourceUsage[]> {
  // ... (existing fetchCostData implementation)
}

/**
 * Generates optimization suggestions based on resource usage data.
 *
 * @param resources Array of ResourceUsage objects.
 * @returns Array of Suggestion objects.
 */
export function generateSuggestions(resources: ResourceUsage[]): Suggestion[] {
  const suggestions: Suggestion[] = [];

  for (const res of resources) {
    // Skip resources with negligible cost
    if (res.cost < THRESHOLDS.minCost) continue;

    // Idle resource detection
    if (
      res.idleTimeHours !== undefined &&
      res.usageAmount > 0 &&
      (res.idleTimeHours / res.usageAmount) * 100 > THRESHOLDS.idleTimePct
    ) {
      suggestions.push({
        resourceId: res.resourceId,
        recommendation: "Consider stopping or terminating this resource.",
        details: `Idle for ${res.idleTimeHours}h out of ${res.usageAmount} usage periods.`,
        severity: "high",
      });
    }

    // Right-sizing suggestions
    if (res.averageCPU !== undefined && res.averageCPU < THRESHOLDS.lowCPU) {
      const suggestedCost = res.cost * 0.8;
      suggestions.push({
        resourceId: res.resourceId,
        recommendation: `Consider right-sizing this resource to reduce costs by ${(1 - suggestedCost / res.cost) * 100}%.`,
        details: `Current cost: $${res.cost.toFixed(2)}. Suggested cost: $${suggestedCost.toFixed(2)}.`,
        severity: "medium",
      });
    }
  }

  return suggestions;
}

export { AWS };