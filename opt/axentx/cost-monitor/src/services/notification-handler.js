const { sendEmailAlert, sendSlackNotification } = require('./alert-senders');
const { getCostAnomalies } = require('./cost-anomaly-detector');
const { checkIngestionFailures } = require('./ingestion-monitor');

class NotificationHandler {
  constructor(config) {
    this.config = config;
    this.interval = config.checkInterval || 3600000; // Default 1 hour
    this.running = false;
  }

  async start() {
    this.running = true;
    while (this.running) {
      try {
        await this.handleAnomalies();
        await this.handleIngestionIssues();
      } catch (error) {
        console.error('Notification handler error:', error);
      }
      await new Promise(resolve => setTimeout(resolve, this.interval));
    }
  }

  async stop() {
    this.running = false;
  }

  async handleAnomalies() {
    const anomalies = await getCostAnomalies(this.config.sensitivityThreshold);
    anomalies.forEach(anomaly => {
      sendEmailAlert(anomaly);
      sendSlackNotification(anomaly);
    });
  }

  async handleIngestionIssues() {
    const failures = await checkIngestionFailures();
    failures.forEach(failure => {
      sendSlackNotification({
        type: 'ingestion_failure',
        details: failure,
        severity: 'high'
      });
    });
  }
}

module.exports = NotificationHandler;