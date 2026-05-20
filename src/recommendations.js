/**
 * Recommendation Engine (pure function)
 *
 * Input: { needs: string[], budget: number, maxResults?: number }
 * Output: Array of builds (without internal scoring fields)
 *
 * The algorithm:
 *   1️⃣ Filter builds whose price ≤ budget.
 *   2️⃣ Compute a relevance score = number of matching tags.
 *   3️⃣ Discard builds with a score of 0 (no relevance).
 *   4️⃣ Sort by score (desc) then price (asc).
 *   5️⃣ Return the first `maxResults` items.
 */

const { BUILD_CATALOGUE } = require('./catalogue');

const DEFAULT_MAX_RESULTS = 5;

/**
 * Compute relevance score.
 *
 * @param {Object} build – catalogue entry
 * @param {Set<string>} needSet – normalized user needs
 * @returns {number}
 */
function scoreBuild(build, needSet) {
  let score = 0;
  for (const tag of build.tags) {
    if (needSet.has(tag)) score += 1;
  }
  return score;
}

/**
 * Main engine.
 *
 * @param {Object} userInput
 * @param {string[]} userInput.needs – already lower‑cased
 * @param {number}   userInput.budget – positive number
 * @param {number}   [maxResults] – defaults to 5
 * @returns {Object[]} Recommended builds
 */
function getRecommendations(userInput, maxResults = DEFAULT_MAX_RESULTS) {
  // ---- validation (defensive, not a substitute for UserInput)
  if (
    !userInput ||
    !Array.isArray(userInput.needs) ||
    typeof userInput.budget !== 'number' ||
    userInput.budget <= 0
  ) {
    throw new Error(
      'Invalid user input: { needs: string[], budget: positive number } required'
    );
  }

  const needSet = new Set(userInput.needs.map((n) => n.toLowerCase()));

  // 1️⃣ budget filter
  const affordable = BUILD_CATALOGUE.filter((b) => b.price <= userInput.budget);

  // 2️⃣ scoring + 3️⃣ discard zero‑score
  const scored = affordable
    .map((b) => ({
      ...b,
      _score: scoreBuild(b, needSet),
    }))
    .filter((b) => b._score > 0);

  // 4️⃣ sort
  scored.sort((a, b) => {
    if (b._score !== a._score) return b._score - a._score; // higher score first
    return a.price - b.price; // cheaper first on tie
  });

  // 5️⃣ slice & strip internal field
  return scored.slice(0, maxResults).map(({ _score, ...rest }) => rest);
}

// Export helpers for testing / future customisation
module.exports = {
  getRecommendations,
  scoreBuild,
  DEFAULT_MAX_RESULTS,
};