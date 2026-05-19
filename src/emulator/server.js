const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const metricsRouter = require('./routes/metrics');

const app = express();

// Security & Headers
app.use(helmet());

// CORS Configuration
app.use(cors());

// Body Parsing
app.use(express.json());

// API Routes
app.use(metricsRouter);

// Server Start
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});