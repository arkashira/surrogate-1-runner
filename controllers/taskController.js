const taskService = require('../services/taskService');

exports.updateStatus = async (req, res) => {
  try {
    const taskId = req.params.id;
    const newStatus = req.body.status;

    await taskService.updateTaskStatus(taskId, newStatus);

    res.status(200).json({ message: 'Task status updated successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};