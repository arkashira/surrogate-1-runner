/**
 * Simple cost forecasting module.
 *
 * The forecast algorithm uses the last three months of usage data
 * to compute an average and applies a 20% growth factor to predict
 * the next month’s cost.
 *
 * The module exports two functions:
 *   - getHistoricalUsage: fetches usage data from the backend.
 *   - forecastCost: calculates the forecast based on the data.
 */

export async function getHistoricalUsage() {
  try {
    const res = await fetch('/api/usage');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    // Expect data to be an array of numbers (monthly usage in USD)
    if (!Array.isArray(data)) throw new Error('Invalid usage data format');
    return data;
  } catch (err) {
    console.error('Failed to fetch historical usage:', err);
    return [];
  }
}

/**
 * Forecast the next month’s cost.
 *
 * @param {number[]} usageHistory - Array of historical monthly usage values.
 * @returns {number} Forecasted cost for the next month.
 */
export function forecastCost(usageHistory) {
  if (!Array.isArray(usageHistory) || usageHistory.length === 0) return 0;
  const recent = usageHistory.slice(-3);
  const avg = recent.reduce((sum, val) => sum + val, 0) / recent.length;
  const forecast = avg * 1.2; // 20% growth assumption
  return Math.round(forecast * 100) / 100; // round to 2 decimals
}