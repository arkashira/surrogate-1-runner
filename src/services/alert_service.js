const axios = require('axios');
const moment = require('moment');
const { sendNotification } = require('../utils/notification_utils');

class AlertService {
  constructor() {
    this.alerts = [];
    this.alertPreferences = {};
  }

  async fetchAlerts() {
    // Fetch alerts from API
    const response = await axios.get('https://api.axentx.com/alerts');
    this.alerts = response.data;
  }

  setAlertPreference(userId, preference) {
    this.alertPreferences[userId] = preference;
  }

  getAlertPreference(userId) {
    return this.alertPreferences[userId] || 'email'; // Default to email if no preference set
  }

  getUpcomingAlerts() {
    const today = moment();
    return this.alerts.filter(alert => moment(alert.date).isAfter(today));
  }

  async sendComplianceAlert(userId, deadline) {
    const alertDate = moment(deadline).subtract(14, 'days');
    const currentDate = moment();

    if (currentDate.isSameOrAfter(alertDate)) {
      const preference = this.getAlertPreference(userId);
      await sendNotification(userId, `Compliance alert: ${deadline} is approaching!`, preference);
    }
  }

  sendAlert(alert) {
    // Send alert to user
    console.log(`Sending alert for ${alert.title} on ${alert.date}`);
  }
}

module.exports = new AlertService();