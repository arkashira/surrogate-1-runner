const mongoose = require('mongoose');

const ValidationProjectSchema = new mongoose.Schema(
  {
    // Existing fields are defined elsewhere – we only extend the schema.
  },
  { timestamps: true }
);

// ------------------------------------------------------------------
// New: Metrics array for founder‑selected key metrics
// ------------------------------------------------------------------
ValidationProjectSchema.add({
  metrics: [
    {
      name: {
        type: String,
        required: [true, 'Metric name is required'],
        trim: true,
      },
      unit: {
        type: String,
        required: [true, 'Metric unit is required'],
        trim: true,
      },
      target: {
        type: Number,
        required: [true, 'Metric target is required'],
        min: [0, 'Target must be a non‑negative number'],
        validate: {
          validator: Number.isFinite,
          message: (props) => `${props.value} is not a valid numeric target`,
        },
      },
      timeframe: {
        type: String,
        default: null,
        trim: true,
      },
    },
  ],
});

module.exports = mongoose.model('ValidationProject', ValidationProjectSchema);