const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://user:pass@localhost:5432/validation',
  // In production you’d add ssl, pool size, etc.
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};