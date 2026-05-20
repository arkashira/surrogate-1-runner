const nodemailer = require('nodemailer');

async function sendEmailAlert(alertData) {
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    }
  });

  const mailOptions = {
    from: 'cost.optimization@axentx.com',
    to: alertData.recipientEmail,
    subject: 'Cost Optimization Opportunity Identified',
    text: alertData.message
  };

  return transporter.sendMail(mailOptions);
}

module.exports = { sendEmailAlert };