const axios = require('axios');
const cron = require('node-cron');
const { MongoClient } = require('mongodb');
const nodemailer = require('nodemailer');

const IRS_API_URL = 'https://api.irs.gov/rules/latest';
const DB_URI = 'mongodb://localhost:27017';
const DB_NAME = 'axentx';
const COLLECTION_NAME = 'irsRules';
const ADMIN_EMAIL = 'admin@example.com';

let cachedRules = null;

async function fetchIRSRules() {
  try {
    const response = await axios.get(IRS_API_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching IRS rules:', error);
    return null;
  }
}

async function saveRulesToDB(rules) {
  const client = new MongoClient(DB_URI, { useNewUrlParser: true, useUnifiedTopology: true });
  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const collection = db.collection(COLLECTION_NAME);
    await collection.deleteMany({}); // Clear old rules
    await collection.insertOne(rules);
    console.log('Rules saved to DB');
  } finally {
    await client.close();
  }
}

async function getRulesFromDB() {
  const client = new MongoClient(DB_URI, { useNewUrlParser: true, useUnifiedTopology: true });
  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const collection = db.collection(COLLECTION_NAME);
    const rules = await collection.findOne();
    return rules;
  } finally {
    await client.close();
  }
}

function sendEmailNotification(rules) {
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'your-email@gmail.com',
      pass: 'your-password'
    }
  });

  const mailOptions = {
    from: 'your-email@gmail.com',
    to: ADMIN_EMAIL,
    subject: 'IRS Rules Updated',
    text: `The IRS rules have been updated. New rules: ${JSON.stringify(rules)}`
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Error sending email:', error);
    } else {
      console.log('Email sent:', info.response);
    }
  });
}

async function updateRules() {
  const newRules = await fetchIRSRules();
  if (!newRules) return;

  const currentRules = await getRulesFromDB();
  if (!currentRules || JSON.stringify(newRules) !== JSON.stringify(currentRules)) {
    await saveRulesToDB(newRules);
    cachedRules = newRules;
    sendEmailNotification(newRules);
  }
}

cron.schedule('0 0 * * 0', () => {
  console.log('Running weekly IRS rule update...');
  updateRules();
});

module.exports = {
  getLatestRules: async () => {
    if (!cachedRules) {
      cachedRules = await getRulesFromDB();
    }
    return cachedRules;
  }
};