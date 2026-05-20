const config = {
  // Historical cost data analysis parameters
  historicalDataWindow: '30 days', // Adjust based on available data and requirements
  sigmaThreshold: 3, // 3σ deviation threshold for anomaly detection

  // Alerting configuration
  alertInterval: 5 * 60 * 1000, // 5 minutes in milliseconds
  slackWebhookUrl: process.env.SLACK_WEBHOOK_URL || '', // Ensure this is set in environment variables

  // Root cause suggestion configuration
  rootCauseSuggestions: [
    'Check recent resource usage',
    'Review recent deployments or changes',
    'Investigate potential billing errors'
  ]
};

module.exports = config;