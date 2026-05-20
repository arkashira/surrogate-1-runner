/**
 * Web‑shell UI entry point.
 *
 * 1. Serves static files from `public/`.
 * 2. Applies the `isAuthorized` middleware before any request is handled.
 * 3. Exposes a tiny API (`/api/status`) that can be used by the UI.
 *
 * The SAML middleware that populates `req.saml` must be mounted
 * *before* this module in the main application.
 */

const express = require('express');
const path = require('path');
const { isAuthorized } = require('./auth');

const app = express();
const PORT = process.env.PORT || 3000;

// ---------- 1. Static UI ----------
app.use(express.static(path.join(__dirname, 'public')));

// ---------- 2. Authorization ----------
app.use((req, res, next) => {
  if (!isAuthorized(req)) {
    return res
      .status(403)
      .send('Forbidden: You are not authorized to access the web shell.');
  }
  next();
});

// ---------- 3. Sample API ----------
app.get('/api/status', (req, res) => {
  res.json({
    status: 'ok',
    user: req.saml?.nameID ?? 'anonymous',
  });
});

// ---------- 4. Start ----------
app.listen(PORT, () => {
  console.log(`Web shell listening on port ${PORT}`);
});

module.exports = app; // exported for testing