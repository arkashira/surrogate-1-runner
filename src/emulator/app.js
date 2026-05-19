const express = require('express');
const healthRouter = require('./routes/health');

const app = express();
const port = 8080; // Standard port for HTTP services (e.g., proxies, sandboxes)

// Mount health check route under /health base path
app.use('/health', healthRouter);

// Start the server
app.listen(port, () => {
  console.log(`Sandbox emulator listening at http://localhost:${port}`);
});