
const nodemailer = require('nodemailer');

class NotificationService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      secure: process.env.EMAIL_SECURE,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
      },
    });
  }

  async sendNotification(to, subject, text) {
    await this.transporter.sendMail({
      from: process.env.EMAIL_FROM,
      to,
      subject,
      text,
    });
  }
}

module.exports = NotificationService;

// api/routes/notifications.js

const express = require('express');
const router = express.Router();
const notificationService = require('../services/notificationService');

router.post('/investment-status-update', async (req, res) => {
  const { investorEmail, status } = req.body;

  try {
    await notificationService.sendNotification(investorEmail, 'Investment Status Update', `Your investment match status has been updated to: ${status}`);
    res.status(200).send('Notification sent successfully');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error sending notification');
  }
});

module.exports = router;