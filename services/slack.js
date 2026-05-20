const { WebClient } = require('@slack/web-api');
const Task = require('../models/Task');

class SlackService {
  constructor(token) {
    this.slack = new WebClient(token);
  }

  async createTaskSlashCommand(command, user) {
    const { text, user_id } = command;
    const [title, description, assignee, priority] = text.split('|').map(item => item.trim());

    const task = new Task({
      title,
      description,
      assignee,
      priority,
      status: 'pending',
      createdBy: user_id
    });

    await task.save();

    // Send notifications
    await this.sendEmailNotification(assignee, task);
    await this.sendSlackNotification(assignee, task);

    return {
      response_action: 'clear',
      text: `Task "${title}" created successfully!`
    };
  }

  async sendEmailNotification(assignee, task) {
    // Implement email notification logic
    console.log(`Email notification sent to ${assignee} for task: ${task.title}`);
  }

  async sendSlackNotification(assignee, task) {
    await this.slack.chat.postMessage({
      channel: assignee,
      text: `You have been assigned a new task: ${task.title}\nDescription: ${task.description}\nPriority: ${task.priority}`
    });
  }
}

module.exports = SlackService;