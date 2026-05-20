const express = require('express');
const router = express.Router();
const { LLMClient } = require('../services/llmClient');
const { validateSpec } = require('../services/specValidator');

const llmClient = new LLMClient();

router.post('/preview', async (req, res) => {
  try {
    const { spec } = req.body;

    // Validate the spec before sending to LLM
    const validationResult = validateSpec(spec);
    if (!validationResult.valid) {
      return res.status(400).json({
        error: 'Invalid spec',
        details: validationResult.errors
      });
    }

    // Call the LLM with the spec
    const previewResult = await llmClient.preview(spec);

    // Check for hallucinations
    const hallucinations = previewResult.hallucinations || [];

    res.json({
      result: previewResult.result,
      hallucinations: hallucinations
    });
  } catch (error) {
    console.error('Error in preview endpoint:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;