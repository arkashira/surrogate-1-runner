const nodemailer = require('nodemailer');
const smtpTransport = require('nodemailer-smtp-transport');

// Securely manage credentials using environment variables or a secrets manager
const transporter = nodemailer.createTransport(smtpTransport({
  host: process.env.SMTP_HOST || 'smtp.gmail.com',
  port: parseInt(process.env.SMTP_PORT) || 587,
  secure: false, // true for 465, false for other ports
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
}));

function sendAlert(email, message) {
  const mailOptions = {
    from: process.env.EMAIL_FROM || 'your-email@gmail.com',
    to: email,
    subject: 'Non-Compliance Alert',
    text: message
  };

  return new Promise((resolve, reject) => {
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error('Error sending email:', error);
        reject(error);
      } else {
        console.log('Email sent: ' + info.response);
        resolve(info);
      }
    });
  });
}

module.exports = { sendAlert };