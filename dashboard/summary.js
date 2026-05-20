const express = require('express');
const router = express.Router();

/**
 * Generates a mock dashboard summary.
 *
 * In a real implementation this would aggregate data from the
 * cost‑tracking datastore. For now we return static data that
 * satisfies the acceptance criteria:
 *   - total monthly cost
 *   - top 5 cost categories
 *   - cost trend over time
 *
 * @returns {Object} summary payload
 */
function getMockSummary() {
  return {
    // Total cost for the current month (USD)
    totalMonthlyCost: 1245.78,

    // Top 5 cost categories ordered by descending cost
    topCategories: [
      { category: 'Compute', cost: 560.12 },
      { category: 'Storage', cost: 310.45 },
      { category: 'Networking', cost: 180.33 },
      { category: 'Database', cost: 120.00 },
      { category: 'Support', cost: 75.00 },
    ],

    // Monthly cost trend for the last 6 months
    costTrend: [
      { month: '2023-11', cost: 1100.00 },
      { month: '2023-12', cost: 1150.50 },
      { month: '2024-01', cost: 1195.20 },
      { month: '2024-02', cost: 1245.78 },
      { month: '2024-03', cost: 1220.40 },
      { month: '2024-04', cost: 1245.78 },
    ],
  };
}

/**
 * GET /dashboard/summary
 *
 * Returns a JSON payload containing the dashboard cost summary.
 */
router.get('/', (req, res) => {
  const summary = getMockSummary();
  res.json(summary);
});

module.exports = router;