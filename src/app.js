const express = require('express');
const integrationRouter = require('./api/integration-api');

const app = express();

// Mount integration API under /api/integration
app.use('/api/integration', integrationRouter);

// Export for serverless or direct start
module.exports = app;

// If executed directly, start an HTTP server (useful for local testing)
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    // eslint-disable-next-line no-console
    console.log(`Surrogate‑1 API listening on port ${PORT}`);
  });
}