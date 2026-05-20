const express = require('express');
const router = express.Router();
const Tool = require('../models/tool');

router.post('/connect', async (req, res) => {
  try {
    const { toolId, userId } = req.body;
    const tool = await Tool.findById(toolId);
    if (!tool) {
      return res.status(404).send({ message: 'Tool not found' });
    }
    // Automate tool connection process with minimal user input
    const connectionResult = await tool.connect(userId);
    if (connectionResult.success) {
      return res.send({ message: 'Tool connected successfully' });
    } else {
      return res.status(500).send({ message: 'Failed to connect tool' });
    }
  } catch (error) {
    console.error(error);
    return res.status(500).send({ message: 'Internal server error' });
  }
});

router.get('/connected', async (req, res) => {
  try {
    const { userId } = req.query;
    const tools = await Tool.find({ userId });
    return res.send(tools);
  } catch (error) {
    console.error(error);
    return res.status(500).send({ message: 'Internal server error' });
  }
});

module.exports = router;