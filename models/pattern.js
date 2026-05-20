const mongoose = require('mongoose');

const PatternSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: String,
  applicationType: { type: String, enum: ['web', 'microservices', 'other'], required: true },
  k8sVersion: { type: String, required: true },
  solution: { type: String, required: true },
  votes: { type: Number, default: 0 },
});

module.exports = mongoose.model('Pattern', PatternSchema);