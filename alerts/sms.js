const twilio = require('twilio');

async function sendSMSAlert(alertData) {
  const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

  const message = await client.messages.create({
    body: alertData.message,
    from: process.env.TWILIO_PHONE_NUMBER,
    to: alertData.recipientPhone
  });

  return message.sid;
}

module.exports = { sendSMSAlert };