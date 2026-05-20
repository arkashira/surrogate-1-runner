const express = require('express');
const path = require('path');
const apiRoutes = require('./api/routes');

const app = express();

// Middleware
app.use(express.json());

// API routes
app.use('/api', apiRoutes);

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// Redirects for better UX
app.get('/credits', (req, res) => {
  res.redirect('/credits-dashboard.html');
});

app.get('/credits/history', (req, res) => {
  res.redirect('/credits-history.html');
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Credit Balance API running on port ${PORT}`);
  });
}

module.exports = app;