class Task {
  constructor(id, title, description, status, priority, dueDate, projectId, userId) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.status = status;
    this.priority = priority;
    this.dueDate = dueDate;
    this.projectId = projectId;
    this.userId = userId;
  }

  static async getAll(userId) {
    // Assuming there's an API endpoint to get all tasks for a user
    const response = await axios.get(`/api/tasks?userId=${userId}`);
    return response.data.map(taskData => new Task(
      taskData.id,
      taskData.title,
      taskData.description,
      taskData.status,
      taskData.priority,
      taskData.dueDate,
      taskData.projectId,
      taskData.userId
    ));
  }

  static async update(taskId, updates) {
    await axios.put(`/api/tasks/${taskId}`, updates);
  }
}

export default Task;