const Task = require('../models/Task');
const slack = require('./slack');

async function updateTaskStatus(taskId, newStatus) {
  const task = await Task.findById(taskId);
  if (!task) {
    throw new Error('Task not found');
  }

  task.status = newStatus;
  await task.save();

  // Notify assignee about the status change
  if (task.assignee) {
    slack.notifyAssignee(task.assignee, task, newStatus);
  }
}

module.exports = {
  updateTaskStatus,
};