const nodemailer = require('nodemailer');
const config = require('../config');

class EmailService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: config.email.user,
        pass: config.email.password,
      },
    });
  }

  async sendTaskCreationNotification(task) {
    const mailOptions = {
      from: config.email.from,
      to: task.assignee.email,
      subject: `New Task Assigned: ${task.title}`,
      text: `You have been assigned a new task:\n\nTitle: ${task.title}\nDescription: ${task.description}\nPriority: ${task.priority}\n\nView task: ${config.frontend.url}/tasks/${task.id}`,
    };

    try {
      await this.transporter.sendMail(mailOptions);
      console.log(`Email notification sent to ${task.assignee.email}`);
    } catch (error) {
      console.error(`Error sending email notification: ${error}`);
    }
  }
}

module.exports = new EmailService();