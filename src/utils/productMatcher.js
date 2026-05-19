/**
 * Utility for computing similarity between two products.
 *
 * The similarity metric is a weighted combination of:
 *   - Jaccard similarity of feature sets
 *   - Category match (binary)
 *   - Price proximity (inverse of absolute difference)
 *
 * The function returns a score between 0 and 1.
 */

const DEFAULT_PRICE_WEIGHT = 0.2;
const DEFAULT_FEATURE_WEIGHT = 0.5;
const DEFAULT_CATEGORY_WEIGHT = 0.3;

/**
 * Compute Jaccard similarity between two sets of strings.
 * @param {Set<string>} setA
 * @param {Set<string>} setB
 * @returns {number} similarity in [0,1]
 */
function jaccardSimilarity(setA, setB) {
  if (setA.size === 0 && setB.size === 0) return 1;
  const intersection = new Set([...setA].filter((x) => setB.has(x)));
  const union = new Set([...setA, ...setB]);
  return intersection.size / union.size;
}

/**
 * Compute similarity between two products.
 *
 * @param {Object} productA - { features: string[], category: string, price: number }
 * @param {Object} productB - same shape as productA
 * @param {Object} [options] - optional weights
 * @returns {number} similarity score in [0,1]
 */
function computeSimilarity(productA, productB, options = {}) {
  const {
    priceWeight = DEFAULT_PRICE_WEIGHT,
    featureWeight = DEFAULT_FEATURE_WEIGHT,
    categoryWeight = DEFAULT_CATEGORY_WEIGHT,
  } = options;

  const featuresA = new Set(productA.features || []);
  const featuresB = new Set(productB.features || []);

  const featureSim = jaccardSimilarity(featuresA, featuresB);
  const categorySim = productA.category === productB.category ? 1 : 0;

  const priceDiff = Math.abs((productA.price || 0) - (productB.price || 0));
  const maxPrice = Math.max(productA.price || 0, productB.price || 0, 1);
  const priceSim = 1 - Math.min(priceDiff / maxPrice, 1);

  const score =
    featureWeight * featureSim +
    categoryWeight * categorySim +
    priceWeight * priceSim;

  return Math.min(Math.max(score, 0), 1);
}

module.exports = {
  computeSimilarity,
  jaccardSimilarity,
};