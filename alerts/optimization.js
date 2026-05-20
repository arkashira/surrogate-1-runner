/**
 * Cost Optimization Alert Module
 *
 * This module provides functionality to send alerts via email and SMS
 * when a cost optimization opportunity is identified.
 *
 * Environment Variables:
 *   EMAIL_HOST      - SMTP host
 *   EMAIL_PORT      - SMTP port
 *   EMAIL_USER      - SMTP username
 *   EMAIL_PASS      - SMTP password
 *   EMAIL_FROM      - Email address to send from
 *   EMAIL_TO        - Comma-separated list of email recipients
 *
 *   TWILIO_ACCOUNT_SID - Twilio Account SID
 *   TWILIO_AUTH_TOKEN  - Twilio Auth Token
 *   TWILIO_FROM        - Twilio phone number to send SMS from
 *   SMS_TO             - Comma-separated list of phone numbers to send SMS to
 *
 * The module exports a single function `triggerOptimizationAlert(opportunity)`
 * which sends an email and SMS with the opportunity details.
 */

const nodemailer = require('nodemailer');
const { Twilio } = require('twilio');
const util = require('util');

// Helper to create a nodemailer transporter if email config is present
function createEmailTransporter() {
  const { EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS } = process.env;
  if (!EMAIL_HOST || !EMAIL_PORT) {
    return null;
  }
  return nodemailer.createTransport({
    host: EMAIL_HOST,
    port: Number(EMAIL_PORT),
    secure: Number(EMAIL_PORT) === 465, // true for 465, false for other ports
    auth: {
      user: EMAIL_USER,
      pass: EMAIL_PASS,
    },
  });
}

// Helper to create a Twilio client if SMS config is present
function createTwilioClient() {
  const { TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN } = process.env;
  if (!TWILIO_ACCOUNT_SID || !TWILIO_AUTH_TOKEN) {
    return null;
  }
  return new Twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);
}

/**
 * Formats the opportunity object into a readable string.
 * @param {Object} opportunity
 * @returns {string}
 */
function formatOpportunity(opportunity) {
  const {
    title = 'Cost Optimization Opportunity',
    description = '',
    potentialSavings = 0,
    resource = '',
    details = {},
  } = opportunity;

  const detailsStr = Object.entries(details)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  return `
${title}

Description: ${description}
Resource: ${resource}
Potential Savings: $${potentialSavings.toFixed(2)}

Details:
${detailsStr}
`.trim();
}

/**
 * Sends an email alert about the opportunity.
 * @param {Object} opportunity
 * @returns {Promise<void>}
 */
async function sendEmailAlert(opportunity) {
  const transporter = createEmailTransporter();
  if (!transporter) {
    console.warn('Email configuration missing; skipping email alert.');
    return;
  }

  const { EMAIL_FROM, EMAIL_TO } = process.env;
  if (!EMAIL_FROM || !EMAIL_TO) {
    console.warn('Email FROM or TO address missing; skipping email alert.');
    return;
  }

  const mailOptions = {
    from: EMAIL_FROM,
    to: EMAIL_TO.split(',').map((s) => s.trim()),
    subject: `Cost Optimization Alert: ${opportunity.title || 'Opportunity'}`,
    text: formatOpportunity(opportunity),
  };

  try {
    await transporter.sendMail(mailOptions);
    console.info('Cost optimization email alert sent.');
  } catch (err) {
    console.error('Failed to send cost optimization email alert:', err);
  }
}

/**
 * Sends an SMS alert about the opportunity.
 * @param {Object} opportunity
 * @returns {Promise<void>}
 */
async function sendSmsAlert(opportunity) {
  const client = createTwilioClient();
  if (!client) {
    console.warn('Twilio configuration missing; skipping SMS alert.');
    return;
  }

  const { TWILIO_FROM, SMS_TO } = process.env;
  if (!TWILIO_FROM || !SMS_TO) {
    console.warn('Twilio FROM or SMS_TO missing; skipping SMS alert.');
    return;
  }

  const messageBody = formatOpportunity(opportunity);

  const toNumbers = SMS_TO.split(',').map((s) => s.trim());

  // Limit to 1600 characters per SMS (Twilio's limit)
  const truncatedBody = messageBody.length > 1600
    ? `${messageBody.substring(0, 1597)}...`
    : messageBody;

  const sendPromises = toNumbers.map((to) =>
    client.messages.create({
      body: truncatedBody,
      from: TWILIO_FROM,
      to,
    })
  );

  try {
    await Promise.all(sendPromises);
    console.info('Cost optimization SMS alert sent.');
  } catch (err) {
    console.error('Failed to send cost optimization SMS alert:', err);
  }
}

/**
 * Triggers cost optimization alerts via email and SMS.
 * @param {Object} opportunity - The cost optimization opportunity details.
 * @returns {Promise<void>}
 */
async function triggerOptimizationAlert(opportunity) {
  if (!opportunity || typeof opportunity !== 'object') {
    throw new Error('Invalid opportunity object');
  }

  // Validate required fields
  if (!opportunity.title || !opportunity.description || opportunity.potentialSavings === undefined) {
    throw new Error('Opportunity object missing required fields (title, description, potentialSavings)');
  }

  await Promise.all([sendEmailAlert(opportunity), sendSmsAlert(opportunity)]);
}

module.exports = {
  triggerOptimizationAlert,
  sendEmailAlert,
  sendSmsAlert,
  formatOpportunity,
};