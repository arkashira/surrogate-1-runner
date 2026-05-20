/**
 * Tool Model
 *
 * Represents a creator's tool or workflow in the system.
 * Uses Mongoose for persistence.
 */

const mongoose = require('mongoose');

const ToolSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, unique: true, trim: true },
    description: { type: String, default: '', trim: true },
    config: { type: mongoose.Schema.Types.Mixed, default: {} },
  },
  {
    timestamps: { createdAt: 'createdAt', updatedAt: false },
  }
);

module.exports = mongoose.model('Tool', ToolSchema);