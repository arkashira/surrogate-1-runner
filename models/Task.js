const emailService = require('../services/email');

class Task {
  constructor(title, description, assignee, priority) {
    this.id = Date.now().toString();
    this.title = title;
    this.description = description;
    this.assignee = assignee;
    this.priority = priority;
    this.status = 'pending';
    this.createdAt = new Date();
  }

  async save() {
    // Save task to database or storage
    console.log(`Task ${this.id} saved`);

    // Send notification
    await emailService.sendTaskCreationNotification(this);
  }
}

module.exports = Task;