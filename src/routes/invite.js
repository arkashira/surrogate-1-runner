const express = require('express');
const router = express.Router();
const EmailService = require('../services/emailService');
const emailService = new EmailService();

router.post('/invite', async (req, res) => {
  const { emails } = req.body;

  if (!emails || emails.length === 0) {
    return res.status(400).send({ message: 'No emails provided' });
  }

  if (emails.length > 10) {
    return res.status(400).send({ message: 'Cannot invite more than 10 team members at once' });
  }

  const signupLink = 'https://example.com/signup'; // Replace with actual signup link

  try {
    for (const email of emails) {
      await emailService.sendInviteEmail(email, signupLink);
    }
    res.status(200).send({ message: 'Invitations sent successfully' });
  } catch (error) {
    res.status(500).send({ message: 'Failed to send invitations', error: error.message });
  }
});

module.exports = router;