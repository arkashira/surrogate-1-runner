const express = require('express');
const router = express.Router({ mergeParams: true }); // inherit :projectId & :metricId from parent
const {
  getObservations,
  createObservation,
} = require('../controllers/observationController');

// OPTIONAL: protect routes – replace with your own auth middleware
// const { requireAuth } = require('../middleware/auth');
// router.use(requireAuth);

router.get('/', getObservations);
router.post('/', createObservation);

module.exports = router;