const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');

const app = express();
app.use(bodyParser.json());

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'sample',
  password: 'secret',
  port: 5432,
});

app.get('/api/hello', (req, res) => {
  res.send('Hello, World!');
});

app.post('/api/data', async (req, res) => {
  const { name, value } = req.body;
  await pool.query('INSERT INTO test (name, value) VALUES ($1, $2)', [name, value]);
  res.send('Data received');
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});