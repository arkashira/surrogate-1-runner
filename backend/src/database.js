/**
 * src/database.js
 *
 * Tiny SQLite‑based store for logging user‑interactions.
 * ----------------------------------------------------
 * • Creates the DB file on first run (in ./data/interactions.db)
 * • Guarantees the `interactions` table exists
 * • Exposes three async helpers:
 *     – logInteraction(userId, type, metadata?)
 *     – getUserInteractions(userId)
 *     – getAllInteractions(filter = {})
 * • All helpers return native Promises, so they can be awaited.
 * • Errors are bubbled up as proper Exceptions.
 * • The DB connection is closed gracefully on process exit.
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// ---------------------------------------------------------------------------
// 1️⃣ Initialise the database (singleton)
const dbPath = path.join(__dirname, '..', 'data', 'interactions.db');

// Ensure the ./data folder exists – otherwise sqlite will throw.
fs.mkdirSync(path.dirname(dbPath), { recursive: true });

const db = new sqlite3.Database(dbPath, err => {
  if (err) {
    console.error('❌ Failed to open SQLite DB:', err);
    process.exit(1);
  }
});

/**
 * Create the `interactions` table if it does not already exist.
 * The schema mirrors the original proposals, with a tiny tweak:
 *   – `metadata` is stored as TEXT (JSON string) but we also add a
 *     `CHECK (json_valid(metadata))` guard for SQLite ≥3.38.
 */
db.serialize(() => {
  const createTableSQL = `
    CREATE TABLE IF NOT EXISTS interactions (
      id               INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id          TEXT    NOT NULL,
      interaction_type TEXT    NOT NULL,
      timestamp        DATETIME DEFAULT CURRENT_TIMESTAMP,
      metadata         TEXT,
      CHECK (metadata IS NULL OR json_valid(metadata))
    );
  `;
  db.run(createTableSQL, err => {
    if (err) console.error('❌ Could not create interactions table:', err);
  });
});

// ---------------------------------------------------------------------------
// 2️⃣ Helper – run a statement and return a Promise
function runAsync(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (err) {
      if (err) return reject(err);
      // `this` is the statement context; expose lastID & changes
      resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
}

// ---------------------------------------------------------------------------
// 3️⃣ Public API
/**
 * Log a new interaction.
 *
 * @param {string} userId            – Identifier of the user.
 * @param {string} interactionType   – e.g. "click", "search", "feedback".
 * @param {object|null} metadata     – Optional extra data (will be JSON‑stringified).
 * @returns {Promise<number>}        – Resolves with the inserted row id.
 */
async function logInteraction(userId, interactionType, metadata = null) {
  const sql = `
    INSERT INTO interactions (user_id, interaction_type, metadata)
    VALUES (?, ?, ?);
  `;
  const metaString = metadata ? JSON.stringify(metadata) : null;
  const { lastID } = await runAsync(sql, [userId, interactionType, metaString]);
  return lastID;
}

/**
 * Retrieve *all* interactions for a single user, newest first.
 *
 * @param {string} userId
 * @returns {Promise<Array<Object>>}
 */
function getUserInteractions(userId) {
  const sql = `
    SELECT *
    FROM interactions
    WHERE user_id = ?
    ORDER BY timestamp DESC;
  `;
  return new Promise((resolve, reject) => {
    db.all(sql, [userId], (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
}

/**
 * Retrieve interactions with optional filtering.
 *
 * @param {Object} filter
 *   - filter.userId          {string}
 *   - filter.interactionType {string}
 *   - filter.since           {Date|string}  (inclusive)
 *   - filter.until           {Date|string}  (inclusive)
 * @returns {Promise<Array<Object>>}
 */
function getAllInteractions(filter = {}) {
  let sql = 'SELECT * FROM interactions';
  const params = [];

  // Build WHERE clause dynamically
  const clauses = [];

  if (filter.userId) {
    clauses.push('user_id = ?');
    params.push(filter.userId);
  }
  if (filter.interactionType) {
    clauses.push('interaction_type = ?');
    params.push(filter.interactionType);
  }
  if (filter.since) {
    clauses.push('timestamp >= ?');
    params.push(new Date(filter.since).toISOString());
  }
  if (filter.until) {
    clauses.push('timestamp <= ?');
    params.push(new Date(filter.until).toISOString());
  }

  if (clauses.length) {
    sql += ' WHERE ' + clauses.join(' AND ');
  }

  sql += ' ORDER BY timestamp DESC;';

  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
}

// ---------------------------------------------------------------------------
// 4️⃣ Graceful shutdown – close the DB when the Node process ends.
function closeDatabase() {
  db.close(err => {
    if (err) console.error('❌ Error closing SQLite DB:', err);
    else console.log('✅ SQLite DB connection closed.');
  });
}
process.on('SIGINT', () => {
  closeDatabase();
  process.exit(0);
});
process.on('SIGTERM', closeDatabase);
process.on('exit', closeDatabase);

// ---------------------------------------------------------------------------
// 5️⃣ Export the public functions
module.exports = {
  logInteraction,
  getUserInteractions,
  getAllInteractions,
  // Exported for testing / advanced use‑cases
  _rawDb: db,
  closeDatabase,
};