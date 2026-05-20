const nodemailer = require('nodemailer');

class EmailService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      }
    });
  }

  async sendInviteEmail(toEmail, signupLink) {
    const mailOptions = {
      from: 'noreply@axentx.com',
      to: toEmail,
      subject: 'Invitation to Join AxentX Team',
      text: `You have been invited to join our team. Please click the following link to sign up: ${signupLink}`
    };

    try {
      await this.transporter.sendMail(mailOptions);
      console.log(`Email sent to ${toEmail}`);
    } catch (error) {
      console.error('Error sending email:', error);
      throw error;
    }
  }
}

module.exports = EmailService;