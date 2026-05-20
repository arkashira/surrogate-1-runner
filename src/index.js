
const { setRequestType, dispatchRequest } = require('./router');

async function handleRequest(request) {
  await setRequestType(request);
  await dispatchRequest(request);
}

// Assuming an Express.js app
const express = require('express');
const app = express();

app.post('/request', (req, res) => {
  const request = req.body;
  handleRequest(request).then(() => {
    res.sendStatus(200);
  });
});