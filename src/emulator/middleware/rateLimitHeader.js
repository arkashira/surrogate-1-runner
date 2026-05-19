/**
 * Adds X-RateLimit-Limit to every response.
 *
 * If an upstream rate‑limit middleware sets `req.rateLimit`,
 * we forward its `limit` value. Otherwise we fall back to a
 * configurable constant (default: 1000 requests per minute).
 */
const DEFAULT_LIMIT = 1000; // safe default; adjust to your env

module.exports = (options = {}) => (req, res, next) => {
  const limit = (req.rateLimit && req.rateLimit.limit) || options.limit || DEFAULT_LIMIT;
  res.set('X-RateLimit-Limit', String(limit));
  next();
};