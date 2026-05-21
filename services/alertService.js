const nodemailer = require('nodemailer');
const axios = require('axios');
const { detectAnomalies } = require('../utils/anomalyDetection');

const {
  EMAIL_HOST,
  EMAIL_PORT,
  EMAIL_USER,
  EMAIL_PASS,
  EMAIL_FROM,
  EMAIL_TO,
  SLACK_WEBHOOK_URL,
} = process.env;

// Configure nodemailer transporter if email credentials are present
const transporter =
  EMAIL_HOST && EMAIL_PORT
    ? nodemailer.createTransport({
        host: EMAIL_HOST,
        port: Number(EMAIL_PORT),
        secure: Number(EMAIL_PORT) === 465, // true for 465, false for other ports
        auth: {
          user: EMAIL_USER,
          pass: EMAIL_PASS,
        },
      })
    : null;

/**
 * Sends an email alert.
 * @param {string} subject
 * @param {string} text
 */
async function sendEmailAlert(subject, text) {
  if (transporter) {
    await transporter.sendMail({
      from: '"AxentX Alerts" <alerts@axentx.com>',
      to: EMAIL_TO,
      subject,
      text,
    });
  }
}

/**
 * Sends a Slack alert.
 * @param {string} channel
 * @param {string} text
 */
async function sendSlackAlert(channel, text) {
  if (SLACK_WEBHOOK_URL) {
    const response = await axios.post(SLACK_WEBHOOK_URL, {
      channel,
      text,
    });
    if (response.status !== 200) {
      console.error('Error sending Slack alert:', response.status);
    }
  }
}

class AlertService {
  constructor(emailConfig, slackConfig) {
    this.emailConfig = emailConfig;
    this.slackConfig = slackConfig;
  }

  async sendAlerts(anomalies) {
    const emailSubject = 'Spending Anomaly Detected';
    const emailText = `Anomalies detected at indices: ${anomalies.join(', ')}`;
    await sendEmailAlert(emailSubject, emailText);

    const slackChannel = '#general';
    const slackText = `Anomalies detected at indices: ${anomalies.join(', ')}`;
    await sendSlackAlert(slackChannel, slackText);
  }
}

module.exports = AlertService;