/**
 * Deterministic mock recommendation generator.
 *
 * @param {string} needs   – free‑text description of the user's use‑case.
 * @param {string|number} budget – budget in USD (may be empty or non‑numeric).
 * @returns {Array<Object>}   – list of recommendation objects.
 *
 * Each object contains:
 *   id, title, description, tier, allocatedBudget, components
 *
 * Replace this function with a real API call later – the signature stays the same.
 */
export function generateRecommendations(needs = '', budget = '') {
  const cleanBudget = parseFloat(budget);
  const hasBudget = !isNaN(cleanBudget) && cleanBudget > 0;

  // -----------------------------------------------------------------
  // 1️⃣  Define three tier buckets – you can adjust proportions as you wish.
  // -----------------------------------------------------------------
  const tiers = [
    { id: 'entry',   name: 'Entry‑Level',   proportion: 0.30 },
    { id: 'mid',     name: 'Mid‑Range',     proportion: 0.50 },
    { id: 'high',    name: 'High‑End',      proportion: 0.20 },
  ];

  // -----------------------------------------------------------------
  // 2️⃣  Build a base description that incorporates the free‑text “needs”.
  // -----------------------------------------------------------------
  const needPhrase = needs.trim()
    ? `optimized for ${needs.trim().toLowerCase()}`
    : 'for general use';

  // -----------------------------------------------------------------
  // 3️⃣  Produce a recommendation per tier.
  // -----------------------------------------------------------------
  const recommendations = tiers.map((tier, idx) => {
    const allocated = hasBudget
      ? Math.round(cleanBudget * tier.proportion)
      : null; // budget unknown → we just show the tier name

    const title = `${tier.name} Build`;
    const description = hasBudget
      ? `${title} – $${allocated} – ${needPhrase}`
      : `${title} – ${needPhrase}`;

    // Simple placeholder component list – replace with real data later.
    const components = [
      `CPU: Example ${tier.name} CPU`,
      `GPU: Example ${tier.name} GPU`,
      `RAM: 16 GB DDR4`,
      `Storage: 1 TB NVMe SSD`,
      `Motherboard: Example ${tier.name} MB`,
      `Power Supply: 650 W`,
    ];

    return {
      id: tier.id,
      title,
      description,
      tier: tier.name,
      allocatedBudget: allocated,
      components,
    };
  });

  // -----------------------------------------------------------------
  // 4️⃣  If the user supplied a very low budget, drop the higher tiers
  //     that would be impossible to afford.
  // -----------------------------------------------------------------
  if (hasBudget) {
    if (cleanBudget < 800) return [recommendations[0]];
    if (cleanBudget < 1500) return [recommendations[0], recommendations[1]];
  }

  return recommendations;
}