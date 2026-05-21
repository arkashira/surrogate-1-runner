const mongoose = require('mongoose');

const ValidationProjectSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    name: {
      type: String,
      required: true,
      maxlength: 100,
      trim: true,
    },
    description: {
      type: String,
      required: true,
      maxlength: 100,
      trim: true,
    },
    targetMarket: {
      type: String,
      required: true,
      maxlength: 100,
      trim: true,
    },
    status: {
      type: String,
      enum: ['In-Progress', 'Completed', 'Failed'],
      default: 'In-Progress',
    },
  },
  { timestamps: true } // adds createdAt / updatedAt
);

module.exports = mongoose.model('ValidationProject', ValidationProjectSchema);