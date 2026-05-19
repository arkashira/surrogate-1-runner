const mongoose = require('mongoose');

const VALID_STATUS = ['pending', 'in-progress', 'done'];
const VALID_TRANSITIONS = {
  pending: ['in-progress', 'done'],
  'in-progress': ['done'],
  done: [] // terminal state
};

const taskSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    description: String,
    projectId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Project',
      required: true
    },
    assignee: {
      // The service uses the name `assignee` (not `assignedTo`)
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true
    },
    status: {
      type: String,
      enum: VALID_STATUS,
      default: 'pending',
      required: true
    },
    priority: {
      type: Number,
      min: 1,
      max: 5,
      default: 3
    },
    dueDate: Date
  },
  { timestamps: true }
);

/**
 * Store the previous status so we can validate transitions.
 * Mongoose does not expose `prev` automatically, so we capture it on `init`.
 */
taskSchema.pre('init', function (doc) {
  this._originalStatus = doc.status;
});

/**
 * Validate status transitions on every save / update.
 */
taskSchema.pre('save', function (next) {
  if (!this.isModified('status')) return next();

  const from = this._originalStatus || this.get('status'); // fallback for new docs
  const to = this.status;

  if (!VALID_TRANSITIONS[from]?.includes(to)) {
    return next(
      new Error(`Invalid status transition from "${from}" to "${to}"`)
    );
  }
  next();
});

module.exports = mongoose.model('Task', taskSchema);