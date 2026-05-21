/**
 * Simple auth guard that assumes a prior middleware has attached
 * the authenticated user to `req.user`.  Adjust as needed for JWT, session, etc.
 */
module.exports.ensureAuthenticated = (req, res, next) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
};