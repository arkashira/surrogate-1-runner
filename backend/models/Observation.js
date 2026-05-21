const mongoose = require('mongoose');

const ObservationSchema = new mongoose.Schema(
  {
    projectId: {
      type: mongoose.Schema.Types.ObjectId,
      required: true,
      ref: 'Project',
    },
    metricId: {
      type: mongoose.Schema.Types.ObjectId,
      required: true,
      ref: 'Metric',
    },
    date: {
      type: Date,
      default: Date.now,
    },
    value: {
      type: Number,
      required: true,
    },
    notes: {
      type: String,
      trim: true,
    },
  },
  {
    timestamps: true, // adds createdAt & updatedAt automatically
  }
);

// Optional: compound index for faster look‑ups
ObservationSchema.index({ projectId: 1, metricId: 1, createdAt: -1 });

module.exports = mongoose.model('Observation', ObservationSchema);