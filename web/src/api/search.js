const express = require('express');
const router = express.Router();

// Mock data representing the overload matrix with parameter type signatures
const overloadMatrix = [
  { id: 1, methodSignature: 'methodA(int, string)', version: '1.0.0' },
  { id: 2, methodSignature: 'methodA(string, int)', version: '1.0.0' },
  { id: 3, methodSignature: 'methodB(float, boolean)', version: '1.1.0' }
];

// Endpoint to handle signature-based search
router.get('/search', (req, res) => {
  const query = req.query.q;
  if (!query) {
    return res.status(400).json({ error: 'Search query is required' });
  }

  // Filter the overload matrix based on the full method signature
  const results = overloadMatrix.filter(item =>
    item.methodSignature.toLowerCase().includes(query.toLowerCase())
  );

  res.json(results);
});

module.exports = router;