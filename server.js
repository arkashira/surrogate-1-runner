const express = require('express');
const analyticsRouter = require('./src/api/analyticsRouter');

const app = express();

// ... other middlewares, body parsers, etc.

app.use('/api/analytics', analyticsRouter);

// start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Server listening on ${PORT}`));