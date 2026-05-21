const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const validationRoutes = require('./routes/validation');
const userMiddleware = require('./middleware/user'); // attaches req.user

const app = express();

// --- DB -------------------------------------------------------
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// --- Middleware ------------------------------------------------
app.use(bodyParser.json());
app.use(userMiddleware); // e.g., sets req.user from JWT or session

// --- Routes ----------------------------------------------------
app.use('/api/v1/validation', validationRoutes);

module.exports = app;