const axios = require('axios');
const { calculateAnomaly } = require('./costAnalysis');
const { sendSlackAlert } = require('./slackNotifier');
const config = require('../config/alerts');

async function monitorCosts() {
  const currentCost = await getCurrentCost();
  const isAnomaly = calculateAnomaly(currentCost);

  if (isAnomaly) {
    const alertMessage = generateAlertMessage(currentCost);
    await sendSlackAlert(alertMessage);
  }
}

function generateAlertMessage(currentCost) {
  return `Cost Anomaly Detected: Current Cost ${currentCost}. Possible causes:\n${config.rootCauseSuggestions.join('\n')}`;
}

async function getCurrentCost() {
  // Placeholder for actual cost retrieval logic
  // This should fetch the latest cost data from your billing system
  return 1000; // Example cost value
}

setInterval(monitorCosts, config.alertInterval);

module.exports = { monitorCosts };