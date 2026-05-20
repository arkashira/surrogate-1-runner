const express = require('express');
const bodyParser = require('body-parser');
const auditRouter = require('./api/audit');

const app = express();
app.use(bodyParser.json());

// Mount audit routes
app.use('/audit', auditRouter);

// Optional: health‑check
app.get('/health', (req, res) => res.send('OK'));

module.exports = app;