const express = require('express');
const router = express.Router();

// Mock data representing available versions
const versions = ['1.0.0', '1.1.0', '1.2.0'];

// Endpoint to handle version selection
router.get('/versions', (req, res) => {
  const selectedVersion = req.query.version;

  if (!selectedVersion || !versions.includes(selectedVersion)) {
    return res.status(400).json({ error: 'Invalid version selected' });
  }

  // Return the selected version along with the relevant overload context
  const filteredOverloadMatrix = overloadMatrix.filter(item => item.version === selectedVersion);

  res.json(filteredOverloadMatrix);
});

module.exports = router;