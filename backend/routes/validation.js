const express = require('express');
const router = express.Router();
const validationService = require('../services/validationService');

// GET /api/v1/validation/projects
router.get('/projects', async (req, res, next) => {
  try {
    const projects = await validationService.getProjects();
    res.json({ projects });
  } catch (err) {
    next(err);
  }
});

// POST /api/v1/validation/projects
router.post('/projects', async (req, res, next) => {
  const { name } = req.body;
  if (!name || typeof name !== 'string') {
    return res.status(400).json({ error: 'Name is required and must be a string' });
  }
  try {
    const newProject = await validationService.createProject(name);
    // Emit real‑time event
    if (req.app.get('projectEmitter')) {
      req.app.get('projectEmitter').emit('projectCreated', newProject);
    }
    res.status(201).json(newProject);
  } catch (err) {
    next(err);
  }
});

module.exports = router;