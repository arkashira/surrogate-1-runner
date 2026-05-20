const fs = require('fs');
const path = require('path');

// Path to persistent storage for learning goals.
// Stored alongside the project in a `data` directory.
const DATA_FILE = path.resolve(__dirname, '..', 'data', 'learning_goals.json');

// In‑memory cache to avoid repeated disk reads.
let cache = null;

/**
 * Load the JSON data from disk (or initialise an empty object).
 * Subsequent calls reuse the in‑memory cache.
 */
function loadData() {
  if (cache) return cache;
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    cache = JSON.parse(raw);
  } catch (_) {
    // If the file does not exist or is malformed, start fresh.
    cache = {};
  }
  return cache;
}

/**
 * Persist the current cache to disk.
 */
function saveData() {
  const dir = path.dirname(DATA_FILE);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(DATA_FILE, JSON.stringify(cache, null, 2));
}

/**
 * Validate that a learning goal meets basic constraints.
 * @throws {Error} if validation fails.
 */
function validateGoal(goal) {
  if (typeof goal !== 'string' || goal.trim().length === 0) {
    throw new Error('Learning goal must be a non‑empty string');
  }
  if (goal.length > 200) {
    throw new Error('Learning goal must be 200 characters or fewer');
  }
}

/**
 * Store a learning goal for a given user.
 *
 * @param {string} userId - Unique identifier for the user.
 * @param {string} goal   - The learning goal text.
 * @returns {Promise<Object>} Resolves with the stored record.
 */
async function setLearningGoal(userId, goal) {
  if (!userId) throw new Error('userId is required');
  validateGoal(goal);

  const data = loadData();
  const record = {
    goal: goal.trim(),
    setAt: new Date().toISOString(),
  };
  data[userId] = record;
  saveData();

  return record;
}

/**
 * Retrieve a previously stored learning goal for a user.
 *
 * @param {string} userId - Unique identifier for the user.
 * @returns {Object|null} The stored record or null if none exists.
 */
function getLearningGoal(userId) {
  if (!userId) throw new Error('userId is required');
  const data = loadData();
  return data[userId] || null;
}

module.exports = {
  setLearningGoal,
  getLearningGoal,
};