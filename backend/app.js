require('dotenv').config();
require('express-async-errors'); // must be required before routes

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const notFound = require('./middlewares/notFound');

const app = express();

/* ---------- Middleware ---------- */
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging
app.use(morgan('combined'));

// Rate limiting (adjust values for your traffic)
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 200,            // limit each IP to 200 requests per windowMs
});
app.use(limiter);

/* ---------- Routes ---------- */
app.use('/api', routes);

/* ---------- 404 & Error ---------- */
app.use(notFound);
app.use(errorHandler);

module.exports = app;