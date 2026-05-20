import { getCloudCosts } from './cloud-costs';

interface CostData {
  monthlySpend: number;
  topCostDrivers: { name: string; cost: number }[];
  savingsInsights: string;
}

async function getMonthlySpend(): Promise<number> {
  const costs = await getCloudCosts();
  return costs.reduce((acc, cost) => acc + cost, 0);
}

async function getTopCostDrivers(): Promise<{ name: string; cost: number }[]> {
  const costs = await getCloudCosts();
  return costs
    .sort((a, b) => b - a)
    .slice(0, 5)
    .map((cost, index) => ({ name: `Cost Driver ${index + 1}`, cost }));
}

async function getSavingsInsights(): Promise<string> {
  const costs = await getCloudCosts();
  const averageCost = costs.reduce((acc, cost) => acc + cost, 0) / costs.length;
  return `Average cost: $${averageCost}`;
}

export { getMonthlySpend, getTopCostDrivers, getSavingsInsights };