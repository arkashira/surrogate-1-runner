const mongoose = require('mongoose');

const ProgressTrackingSchema = new mongoose.Schema({
  userId: { type: String, required: true, unique: true },
  metrics: {
    totalAttempts: Number,
    successfulAttempts: Number,
    lastUpdated: Date
  }
});

module.exports = mongoose.model('ProgressTracking', ProgressTrackingSchema);