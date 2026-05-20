const { sendEmailAlert } = require('./email');
const { sendSMSAlert } = require('./sms');

class AlertDelivery {
  constructor() {}

  async deliverAlert(alertData) {
    await this.sendEmailAlert(alertData);
    await this.sendSMSAlert(alertData);
  }

  async sendEmailAlert(alertData) {
    return sendEmailAlert(alertData);
  }

  async sendSMSAlert(alertData) {
    return sendSMSAlert(alertData);
  }
}

module.exports = new AlertDelivery();