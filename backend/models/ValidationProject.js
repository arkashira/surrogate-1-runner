const mongoose = require('mongoose');

const metricSchema = new mongoose.Schema({
  name: { type: String, required: true },
  unit: { type: String, default: 'count' },
  target: { type: Number, required: true },
  timeFrame: { type: String, default: 'monthly' }
});

const validationProjectSchema = new mongoose.Schema({
  // Other project fields...
  metrics: [metricSchema]
});

module.exports = mongoose.model('ValidationProject', validationProjectSchema);