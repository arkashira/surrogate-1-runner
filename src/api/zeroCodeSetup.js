/**
 * Zero-Code Setup API
 *
 * This module exposes an Express router that allows a creator to
 * register a new tool or workflow without writing any code.
 * The API expects a minimal payload and returns a confirmation
 * upon successful creation.
 */

const express = require('express');
const router = express.Router();
const Tool = require('../models/tool');

/**
 * POST /api/zero-code-setup
 *
 * Body:
 *   {
 *     "name": "string",          // required, unique
 *     "description": "string",   // optional
 *     "config": { ... }          // optional, arbitrary JSON
 *   }
 *
 * Response:
 *   201 Created
 *   {
 *     "id": "<mongo-id>",
 *     "name": "...",
 *     "description": "...",
 *     "config": { ... },
 *     "createdAt": "<timestamp>"
 *   }
 *
 * Errors:
 *   400 Bad Request - missing required fields or validation errors
 *   409 Conflict - tool name already exists
 *   500 Internal Server Error - unexpected failures
 */
router.post('/', async (req, res) => {
  try {
    const { name, description = '', config = {} } = req.body;

    // Basic validation
    if (!name || typeof name !== 'string' || name.trim() === '') {
      return res.status(400).json({ error: 'Name is required and must be a non-empty string.' });
    }

    // Check for duplicate name
    const existing = await Tool.findOne({ name: name.trim() }).exec();
    if (existing) {
      return res.status(409).json({ error: 'A tool with this name already exists.' });
    }

    // Create tool
    const tool = await Tool.create({
      name: name.trim(),
      description: description.trim(),
      config,
    });

    // Respond with confirmation
    return res.status(201).json({
      id: tool._id,
      name: tool.name,
      description: tool.description,
      config: tool.config,
      createdAt: tool.createdAt,
    });
  } catch (err) {
    console.error('Zero-code setup error:', err);
    return res.status(500).json({ error: 'Internal server error.' });
  }
});

module.exports = router;