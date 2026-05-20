const nodemailer = require('nodemailer');
const twilio = require('twilio');

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false, // or 'STARTTLS'
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-password'
  }
});

const accountSid = 'your-twilio-account-sid';
const authToken = 'your-twilio-auth-token';
const client = new twilio(accountSid, authToken);

module.exports = {
  sendEmail: (subject, body) => {
    const mailOptions = {
      from: 'your-email@gmail.com',
      to: 'recipient-email@example.com',
      subject,
      text: body
    };
    return transporter.sendMail(mailOptions);
  },
  sendSMS: (phoneNumber, message) => {
    return client.messages
      .create({
        body: message,
        from: 'your-twilio-phone-number',
        to: phoneNumber
      })
      .then(message => message.sid);
  }
};