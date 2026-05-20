const axios = require('axios');
const nodemailer = require('nodemailer');
const twilio = require('twilio');

const THRESHOLD = 1000;
const EMAIL_FROM = 'alerts@example.com';
const EMAIL_TO = 'youremail@example.com';
const TWILIO_ACCOUNT_SID = 'your_twilio_account_sid';
const TWILIO_AUTH_TOKEN = 'your_twilio_auth_token';
const TWILIO_PHONE_NUMBER = '+12345678901';
const RECIPIENT_PHONE_NUMBER = '+09876543210';

async function sendEmail(to, subject, text) {
  let transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: EMAIL_FROM,
      pass: 'your_email_password'
    }
  });

  let mailOptions = {
    from: EMAIL_FROM,
    to: to,
    subject: subject,
    text: text
  };

  await transporter.sendMail(mailOptions);
}

async function sendSMS(to, body) {
  let client = twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);

  await client.messages.create({
    body: body,
    from: TWILIO_PHONE_NUMBER,
    to: to
  });
}

async function checkCost() {
  let response = await axios.get('https://api.your_cloud_provider.com/cost');
  let cost = response.data.total_cost;

  if (cost > THRESHOLD) {
    await sendEmail(EMAIL_TO, 'Cloud Cost Alert', `Your monthly cloud cost is $${cost}`);
    await sendSMS(RECIPIENT_PHONE_NUMBER, `Your monthly cloud cost is $${cost}`);
  }
}

checkCost().catch(console.error);