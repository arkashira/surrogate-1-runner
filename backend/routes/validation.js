const express = require('express');
const router = express.Router();
const ValidationProject = require('../models/validationProject');
const { ensureAuthenticated } = require('../middleware/auth');

// POST /api/v1/validation/projects
router.post(
  '/projects',
  ensureAuthenticated,
  async (req, res) => {
    const { name, description, targetMarket } = req.body;

    // --- Server‑side validation -------------------------------------------------
    if (!name || !description || !targetMarket) {
      return res.status(400).json({
        error: 'Name, description, and target market are required.',
      });
    }

    const tooLong = [name, description, targetMarket].some(
      (field) => field.length > 100
    );
    if (tooLong) {
      return res.status(400).json({
        error: 'All fields must be 100 characters or fewer.',
      });
    }

    // --- Persist ---------------------------------------------------------------
    try {
      const project = new ValidationProject({
        user: req.user._id,
        name,
        description,
        targetMarket,
      });

      const saved = await project.save();

      // --- Response -------------------------------------------------------------
      return res.status(201).json({
        project: saved, // full document (includes _id, timestamps, etc.)
        redirectTo: `/workflow/step-1/${saved._id}`,
      });
    } catch (err) {
      console.error('Error creating validation project:', err);
      return res.status(500).json({ error: 'Internal server error.' });
    }
  }
);

module.exports = router;