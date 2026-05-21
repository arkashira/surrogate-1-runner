const { zScore, rollingStats } = require('../utils/statistics');
const { sendEmailAlert, sendSlackAlert } = require('../utils/alerts');
const { fetchHistoricalData, parseCSV } = require('../utils/dataProcessor');

class AnomalyDetector {
  /**
   * Anomaly detection module for cost monitoring.
   *
   * @param {Object} config - Configuration options
   * @param {string} config.dataSource - URL or file path to historical data
   * @param {number} [config.window=30] - Rolling window size for statistics
   * @param {number} [config.sensitivity=2] - Sensitivity multiplier for stddev
   * @param {string} [config.emailTo] - Email address for alerts
   * @param {string} [config.slackChannel] - Slack channel for alerts
   */
  constructor(config) {
    this.config = {
      window: 30,
      sensitivity: 2,
      emailTo: process.env.ALERT_EMAIL,
      slackChannel: process.env.SLACK_ALERT_CHANNEL,
      ...config
    };
  }

  /**
   * Detect anomalies in cost data
   * @param {Array<{date: string, amount: number}>} data - Cost records
   * @returns {Promise<Array<{date: string, amount: number, mean: number, stddev: number}>>}
   */
  async detectAnomalies(data) {
    if (!Array.isArray(data) || data.length === 0) return [];

    // Get historical data if needed
    const historicalData = await this._getHistoricalData();

    const stats = rollingStats([...historicalData, ...data], this.config.window);
    const anomalies = [];

    for (let i = 0; i < data.length; i++) {
      const record = data[i];
      const { mean, stddev } = stats[historicalData.length + i];
      const threshold = mean + this.config.sensitivity * stddev;

      // Use both z-score and threshold comparison for robustness
      const z = zScore([...historicalData, ...data.slice(0, i + 1)], record);
      const isAnomaly = record.amount > threshold || Math.abs(z) > this.config.sensitivity;

      if (isAnomaly) {
        anomalies.push({
          ...record,
          mean,
          stddev,
          zScore: z,
          threshold
        });

        await this._sendAlerts(record, {
          mean,
          stddev,
          zScore: z,
          threshold
        });
      }
    }

    return anomalies;
  }

  async _getHistoricalData() {
    if (!this.config.dataSource) return [];
    const csvContent = await fetchHistoricalData(this.config.dataSource);
    return parseCSV(csvContent);
  }

  async _sendAlerts(record, stats) {
    const message = this._formatAlertMessage(record, stats);

    if (this.config.emailTo) {
      try {
        await sendEmailAlert({
          to: this.config.emailTo,
          subject: `Cost Anomaly on ${record.date}`,
          text: message
        });
      } catch (e) {
        console.error('Email send failed:', e);
      }
    }

    if (this.config.slackChannel) {
      try {
        await sendSlackAlert({
          channel: this.config.slackChannel,
          text: message
        });
      } catch (e) {
        console.error('Slack send failed:', e);
      }
    }
  }

  _formatAlertMessage(record, stats) {
    return `⚠️ Cost anomaly detected on ${record.date}:\n` +
      `Amount: $${record.amount.toFixed(2)}\n` +
      `Rolling mean: $${stats.mean.toFixed(2)}\n` +
      `Stddev: $${stats.stddev.toFixed(2)}\n` +
      `Z-score: ${stats.zScore.toFixed(2)}\n` +
      `Threshold: $${stats.threshold.toFixed(2)}`;
  }
}

module.exports = AnomalyDetector;