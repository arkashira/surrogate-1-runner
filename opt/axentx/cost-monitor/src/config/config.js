module.exports = {
  sensitivityThreshold: 1.5, // Default 50% deviation
  checkInterval: 3600000, // 1 hour in milliseconds
  emailSettings: {
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    }
  },
  slackWebhookUrl: process.env.SLACK_WEBHOOK_URL,
  recipients: {
    email: 'finance-team@axentx.com',
    slack: '#finance-alerts'
  }
};