/**
 * Express route for handling Workio webhook events.
 *
 * Wires validation middleware and handles the trigger logic
 * for Surrogate-1 ingestion jobs.
 */

const express = require('express');
const router = express.Router();
const validateWorkioPayload = require('../middleware/validation');
const { enqueueIngestionJob } = require('../services/ingestion');

// POST /opt/axentx/surrogate-1/api/workflow-trigger
router.post(
  '/opt/axentx/surrogate-1/api/workflow-trigger',
  express.json(),
  validateWorkioPayload,
  async (req, res) => {
    const { task, data } = req.body;
    const taskId = task.id;

    // Business Logic: Only trigger on task completion
    if (task.status.toLowerCase() !== 'completed') {
      return res.status(200).json({
        message: 'Event received but task is not completed; no action taken',
      });
    }

    try {
      // Pass the task ID and any additional data to the ingestion service
      await enqueueIngestionJob(taskId, data);
      
      return res.status(200).json({
        message: 'Ingestion job enqueued successfully',
      });
    } catch (err) {
      console.error('Failed to enqueue ingestion job:', err);
      return res.status(500).json({
        error: 'Failed to enqueue ingestion job',
        remediation: 'Check server logs for details',
      });
    }
  }
);

module.exports = router;