const express = require('express');
const router = express.Router();

// Mock data representing the overload matrix with parameter type signatures
const overloadMatrix = [
  { id: 1, methodSignature: 'methodA(int, string)', version: '1.0.0' },
  { id: 2, methodSignature: 'methodA(string, int)', version: '1.0.0' },
  { id: 3, methodSignature: 'methodB(float, boolean)', version: '1.1.0' }
];

// Endpoint to display the overload matrix
router.get('/', (req, res) => {
  res.json(overloadMatrix);
});

module.exports = router;