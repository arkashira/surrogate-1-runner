const express = require('express');
const https = require('https');
const fs = require('fs');
const { authenticateToken } = require('./middleware/auth.js');

const app = express();

app.use(authenticateToken);

app.get('/secure-terminal', (req, res) => {
    res.send('Secure terminal interface');
});

const options = {
    key: fs.readFileSync('/opt/axentx/surrogate-1/tls/key.pem'),
    cert: fs.readFileSync('/opt/axentx/surrogate-1/tls/cert.pem')
};

https.createServer(options, app).listen(3000, () => {
    console.log('Server running on port 3000');
});