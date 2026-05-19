const mongoose = require('mongoose');

const taskSchema = new mongoose.Schema({
  title: String,
  description: String,
  status: { type: String, default: 'pending' },
  assignee: String,
});

const Task = mongoose.model('Task', taskSchema);

module.exports = Task;