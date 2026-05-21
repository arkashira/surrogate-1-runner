const Observation = require('../models/Observation');
const asyncHandler = require('express-async-handler'); // <-- handles try/catch for us
const Joi = require('joi'); // or any validator you prefer

// ---------- Validation schema ----------
const createObsSchema = Joi.object({
  value: Joi.number().required(),
  notes: Joi.string().allow('', null),
});

// ---------- GET /projects/:projectId/metrics/:metricId/observations ----------
exports.getObservations = asyncHandler(async (req, res) => {
  const { projectId, metricId } = req.params;
  const { page = 1, limit = 20, sort = '-createdAt' } = req.query;

  const filter = { projectId, metricId };
  const observations = await Observation.find(filter)
    .sort(sort)
    .skip((page - 1) * limit)
    .limit(Number(limit));

  const total = await Observation.countDocuments(filter);

  res.json({
    page: Number(page),
    limit: Number(limit),
    total,
    data: observations,
  });
});

// ---------- POST /projects/:projectId/metrics/:metricId/observations ----------
exports.createObservation = asyncHandler(async (req, res) => {
  // 1️⃣ Validate payload
  const { error, value } = createObsSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ message: error.details[0].message });
  }

  // 2️⃣ Build document
  const observation = new Observation({
    projectId: req.params.projectId,
    metricId: req.params.metricId,
    value: value.value,
    notes: value.notes,
    // `date` defaults to now via schema
  });

  // 3️⃣ Persist
  await observation.save();

  // 4️⃣ Respond
  res.status(201).json(observation);
});