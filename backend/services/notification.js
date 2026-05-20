const nodemailer = require('nodemailer');
const { createInAppNotification } = require('../models/notification');

class NotificationService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      }
    });
  }

  async sendProjectStatusNotification(project, status, metrics, consecutiveDays) {
    const notificationData = {
      projectId: project.id,
      projectName: project.name,
      status,
      metrics,
      consecutiveDays,
      timestamp: new Date().toISOString()
    };

    // Send in-app notification
    await this.sendInAppNotification(notificationData);

    // Send email if enabled
    if (project.emailNotificationsEnabled) {
      await this.sendEmailNotification(notificationData);
    }
  }

  async sendInAppNotification(data) {
    const notification = {
      userId: data.userId,
      type: 'PROJECT_STATUS',
      title: `Project ${data.projectName} is ${data.status}`,
      message: this.generateNotificationMessage(data),
      data: {
        projectId: data.projectId,
        status: data.status,
        metrics: data.metrics,
        consecutiveDays: data.consecutiveDays
      },
      read: false,
      createdAt: new Date()
    };

    await createInAppNotification(notification);
  }

  async sendEmailNotification(data) {
    const subject = `Project ${data.projectName} Status Update: ${data.status}`;
    const text = this.generateEmailContent(data);

    await this.transporter.sendMail({
      from: process.env.EMAIL_FROM,
      to: data.userEmail,
      subject,
      text
    });
  }

  generateNotificationMessage(data) {
    if (data.status === 'At Risk') {
      const failedMetrics = data.metrics.filter(m => !m.passed);
      return `⚠️ ${failedMetrics.length} metric(s) below threshold. Review dashboard.`;
    } else {
      return `✅ All metrics met targets for ${data.consecutiveDays} consecutive days.`;
    }
  }

  generateEmailContent(data) {
    let content = `Project Status Update for ${data.projectName}\n\n`;
    content += `Status: ${data.status}\n`;
    content += `Date: ${new Date().toLocaleDateString()}\n\n`;

    if (data.status === 'At Risk') {
      content += 'Metrics below threshold:\n';
      data.metrics.filter(m => !m.passed).forEach(m => {
        content += `- ${m.name}: ${m.value} (target: ${m.target})\n`;
      });
      content += '\nPlease review your project dashboard.';
    } else {
      content += `All metrics have met or exceeded targets for ${data.consecutiveDays} consecutive days.\n\n`;
      content += 'Continue monitoring your project progress.';
    }

    return content;
  }
}

module.exports = new NotificationService();