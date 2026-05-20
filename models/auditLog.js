const mongoose = require('mongoose');

const AuditLogSchema = new mongoose.Schema({
  modelId: {
    type: String,
    required: true
  },
  input: {
    type: Object,
    required: true
  },
  output: {
    type: Object,
    required: true
  },
  context: {
    type: Object,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('AuditLog', AuditLogSchema);