const mongoose = require('mongoose');

const benchmarkSchema = new mongoose.Schema({
  variant: {
    type: String,
    required: true,
    trim: true
  },
  cloudProvider: {
    type: String,
    required: true,
    enum: ['AWS', 'GCP', 'Azure'],
    trim: true
  },
  coldStartLatency: {
    type: Number,
    required: true,
    min: 0,
    description: 'Average cold start latency in milliseconds'
  },
  peakMemoryConsumption: {
    type: Number,
    required: true,
    min: 0,
    description: 'Peak memory consumption in megabytes'
  },
  benchmarkSource: {
    type: String,
    required: true,
    trim: true,
    description: 'Source attribution for the benchmark data'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

benchmarkSchema.index({ variant: 1, cloudProvider: 1 });

const Benchmark = mongoose.model('Benchmark', benchmarkSchema);

module.exports = Benchmark;