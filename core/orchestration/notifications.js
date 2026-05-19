const nodemailer = require('nodemailer');
const { WebClient } = require('@slack/web-api');
const config = require('./config');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: config.emailUser,
    pass: config.emailPass,
  },
});

const slackClient = new WebClient(config.slackToken);

class Notifier {
  sendEmail(to, subject, text) {
    const mailOptions = {
      from: config.emailFrom,
      to,
      subject,
      text,
    };

    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.log(error);
      } else {
        console.log('Email sent: ' + info.response);
      }
    });
  }

  sendSlackMessage(channel, text) {
    slackClient.chat.postMessage({
      channel,
      text,
    });
  }

  notify(event, condition) {
    if (event === 'agentInteractionIssue' && condition) {
      this.sendEmail(config.developerEmail, 'Agent Interaction Issue', 'An issue has arisen during agent interactions.');
      this.sendSlackMessage(config.developerSlackChannel, 'An issue has arisen during agent interactions.');
    }
  }
}

module.exports = new Notifier();