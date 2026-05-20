const delivery = require('./delivery');
const threshold = require('./threshold');

module.exports = {
  sendAlert: (monthlyCost) => {
    if (threshold.shouldSendAlert(monthlyCost)) {
      delivery.sendEmail('Cloud Cost Alert', `Your monthly cloud cost is $${monthlyCost}.`);
      delivery.sendSMS('+1234567890', `Your monthly cloud cost is $${monthlyCost}.`);
    }
  }
};