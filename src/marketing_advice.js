/**
 * Generates actionable marketing advice based on current metrics.
 *
 * @param {Object} userData
 * @param {Object} userData.metrics
 * @param {number} userData.metrics.clickThroughRate
 * @param {number} userData.metrics.conversionRate
 * @param {number} userData.metrics.bounceRate
 *
 * @returns {Array<Object>} advice list
 */
const { v4: uuidv4 } = require('uuid');

const thresholds = {
  clickThroughRate: 0.05,
  conversionRate: 0.02,
  bounceRate: 0.60
};

const adviceTemplates = [
  {
    key: 'increaseCTR',
    action: 'Optimize headline and CTA placement.',
    expectedImpact: '↑ CTR by ~10‑15%',
    metric: 'clickThroughRate',
    threshold: thresholds.clickThroughRate
  },
  {
    key: 'boostConversion',
    action: 'Add a clear value proposition and social proof.',
    expectedImpact: '↑ Conversion by ~5‑8%',
    metric: 'conversionRate',
    threshold: thresholds.conversionRate
  },
  {
    key: 'reduceBounce',
    action: 'Improve page load speed and mobile responsiveness.',
    expectedImpact: '↓ Bounce by ~7‑12%',
    metric: 'bounceRate',
    threshold: thresholds.bounceRate
  }
];

/**
 * Returns an array of advice objects that are relevant to the current metrics.
 */
function getMarketingAdvice(userData) {
  if (!userData || !userData.metrics) {
    throw new Error('Missing required userData.metrics');
  }

  const { metrics } = userData;
  const advice = [];

  adviceTemplates.forEach(template => {
    const current = metrics[template.metric];
    if (current === undefined) return;

    const needsImprovement =
      (template.metric === 'bounceRate' && current > template.threshold) ||
      (template.metric !== 'bounceRate' && current < template.threshold);

    if (needsImprovement) {
      advice.push({
        id: uuidv4(),
        action: template.action,
        expectedImpact: template.expectedImpact,
        confidence: 0.8 // placeholder, can be tuned by ML
      });
    }
  });

  // If nothing actionable, give a generic recommendation
  if (advice.length === 0) {
    advice.push({
      id: uuidv4(),
      action: 'Run A/B tests on key landing pages.',
      expectedImpact: 'Identify high‑impact changes.',
      confidence: 0.7
    });
  }

  return advice;
}

module.exports = { getMarketingAdvice };