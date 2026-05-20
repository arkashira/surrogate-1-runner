// For SQL (pg) or Mongo (mongoose) – the interface is the same.

module.exports = {
  /**
   * Execute a query or find operation.
   * @param {string} sqlOrFilter – SQL string or Mongo filter
   * @param {Array|Object} params – SQL params or Mongo query options
   * @returns {Promise<Array>} rows / documents
   */
  async query(sqlOrFilter, params) {
    // Example for PostgreSQL:
    // const { Pool } = require('pg');
    // const pool = new Pool({ connectionString: process.env.DATABASE_URL });
    // return (await pool.query(sqlOrFilter, params)).rows;

    // Example for Mongoose:
    // const AuditLog = require('../models/auditLog');
    // return AuditLog.find(sqlOrFilter, null, params).lean();

    throw new Error('DB implementation missing');
  },
};