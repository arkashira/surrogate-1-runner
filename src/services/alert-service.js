const nodemailer = require('nodemailer');
const slack = require('slack');

const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  secure: false, // or 'STARTTLS'
  auth: {
    user: 'username',
    pass: 'password',
  },
});

const sendEmail = (to, subject, body) => {
  const mailOptions = {
    from: 'sender@example.com',
    to,
    subject,
    text: body,
  };
  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });
};

const sendSlackNotification = (channel, text) => {
  slack.chat.postMessage({
    channel,
    text,
  }, (error, response) => {
    if (error) {
      console.log(error);
    } else {
      console.log(response);
    }
  });
};

module.exports = (data, threshold) => {
  const anomalyDetector = require('./anomaly-detector');
  const isAnomaly = anomalyDetector(data, threshold);
  if (isAnomaly) {
    sendEmail('finance@example.com', 'Cost Anomaly Detected', 'Anomaly detected in data');
    sendSlackNotification('general', 'Cost Anomaly Detected');
  }
};