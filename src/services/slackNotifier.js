const axios = require('axios');
const config = require('../config/alerts');

async function sendSlackAlert(message) {
  try {
    await axios.post(config.slackWebhookUrl, {
      text: message
    });
    console.log('Alert sent successfully');
  } catch (error) {
    console.error('Failed to send alert:', error);
  }
}

module.exports = { sendSlackAlert };