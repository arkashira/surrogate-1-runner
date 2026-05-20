const express = require('express');
const router = express.Router();
const { ValidationProject } = require('../models');

// PATCH /api/v1/validation/projects/:id/metrics
router.patch('/:id/metrics', async (req, res) => {
  try {
    const { id } = req.params;
    const { metrics } = req.body;

    if (!metrics || !Array.isArray(metrics)) {
      return res.status(400).json({ error: 'Metrics must be an array' });
    }

    const project = await ValidationProject.findById(id);
    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    // Validate each metric
    const validatedMetrics = metrics.map(metric => {
      if (!metric.name || !metric.target) {
        throw new Error('Each metric must have a name and target');
      }
      if (isNaN(metric.target)) {
        throw new Error('Target must be a number');
      }
      return metric;
    });

    project.metrics = validatedMetrics;
    await project.save();

    res.json({ success: true, project });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router;