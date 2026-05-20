const express = require('express');
const https = require('https');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const { validateToken } = require('./auth-service');

const app = express();
const server = https.createServer({
  key: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/key.pem'),
  cert: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/cert.pem'),
  ca: fs.readFileSync('/opt/axentx/surrogate-1/config/tls/ca.pem')
}, app);

app.use(express.json());

app.post('/terminal', async (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token || !(await validateToken(token))) {
    return res.status(401).send('Invalid token');
  }

  const sessionId = uuidv4();
  // Start a new terminal session here with the sessionId
  // ...

  res.send({ sessionId });
});

server.listen(443, () => {
  console.log('Terminal server listening on port 443');
});