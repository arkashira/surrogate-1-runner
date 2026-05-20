/**
 * Policy Enforcer Service
 *
 * Handles budget enforcement, token limits, and compliance reporting.
 * This implementation uses in-memory storage for simplicity.
 */

const fs = require('fs');
const path = require('path');

/**
 * Load policy configuration from a JSON file or environment variables.
 * Expected structure:
 * {
 *   "models": {
 *     "gpt-4": {
 *       "costPerToken": 0.03,
 *       "budget": 1000,
 *       "alertThreshold": 0.8
 *     },
 *     "gpt-3.5": {
 *       "costPerToken": 0.02,
 *       "budget": 500,
 *       "alertThreshold": 0.9
 *     }
 *   },
 *   "sensitivityLimits": {
 *     "public": 2000,
 *     "internal": 1000,
 *     "confidential": 500
 *   }
 * }
 */
const CONFIG_PATH = path.join(__dirname, '..', '..', 'policy-config.json');
let config = {};

try {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
  config = JSON.parse(raw);
} catch (err) {
  console.warn(`Policy config not found at ${CONFIG_PATH}. Falling back to env vars.`);
  config = {
    models: {
      'gpt-4': {
        costPerToken: parseFloat(process.env.GPT4_COST_PER_TOKEN) || 0.03,
        budget: parseFloat(process.env.GPT4_BUDGET) || 1000,
        alertThreshold: parseFloat(process.env.GPT4_ALERT_THRESHOLD) || 0.8,
      },
      'gpt-3.5': {
        costPerToken: parseFloat(process.env.GPT35_COST_PER_TOKEN) || 0.02,
        budget: parseFloat(process.env.GPT35_BUDGET) || 500,
        alertThreshold: parseFloat(process.env.GPT35_ALERT_THRESHOLD) || 0.9,
      },
    },
    sensitivityLimits: {
      public: parseInt(process.env.PUBLIC_LIMIT) || 2000,
      internal: parseInt(process.env.INTERNAL_LIMIT) || 1000,
      confidential: parseInt(process.env.CONFIDENTIAL_LIMIT) || 500,
    },
  };
}

/**
 * In-memory usage tracker.
 * Structure:
 * {
 *   modelName: {
 *     tokensUsed: number,
 *     costUsed: number
 *   }
 * }
 */
const usageTracker = new Map();

/**
 * Helper to get or initialize usage record for a model.
 */
function getUsageRecord(model) {
  if (!usageTracker.has(model)) {
    usageTracker.set(model, { tokensUsed: 0, costUsed: 0 });
  }
  return usageTracker.get(model);
}

/**
 * Checks if the request would exceed the budget for the model.
 * Returns an object: { allowed: boolean, remainingBudget: number, alert: boolean }
 */
function checkBudget(model, tokens) {
  const modelConfig = config.models[model];
  if (!modelConfig) {
    // Unknown model, allow by default
    return { allowed: true, remainingBudget: Infinity, alert: false };
  }

  const costPerToken = modelConfig.costPerToken;
  const budget = modelConfig.budget;
  const alertThreshold = modelConfig.alertThreshold;

  const usage = getUsageRecord(model);
  const projectedCost = usage.costUsed + tokens * costPerToken;

  if (projectedCost > budget) {
    return { allowed: false, remainingBudget: 0, alert: false };
  }

  const remainingBudget = budget - projectedCost;
  const alert = remainingBudget / budget <= alertThreshold;

  return { allowed: true, remainingBudget, alert };
}

/**
 * Checks if the token usage for the given sensitivity classification
 * would exceed the configured limit.
 * Returns an object: { allowed: boolean, remainingLimit: number }
 */
function checkTokenLimit(sensitivity, tokens) {
  const limit = config.sensitivityLimits[sensitivity];
  if (limit === undefined) {
    // Unknown sensitivity, allow by default
    return { allowed: true, remainingLimit: Infinity };
  }

  // For simplicity, we track per-request limits only.
  // A more robust implementation would track cumulative usage per day.
  if (tokens > limit) {
    return { allowed: false, remainingLimit: 0 };
  }

  return { allowed: true, remainingLimit: limit - tokens };
}

/**
 * Update usage statistics after a successful request.
 */
function recordUsage(model, tokens) {
  const usage = getUsageRecord(model);
  const costPerToken = config.models[model]?.costPerToken || 0;
  usage.tokensUsed += tokens;
  usage.costUsed += tokens * costPerToken;
}

/**
 * Generate a compliance report summarizing usage per model and sensitivity.
 * Returns a plain text report.
 */
function generateComplianceReport() {
  const lines = [];
  lines.push('Compliance Report');
  lines.push('=================');
  lines.push('');

  lines.push('Per-Model Usage:');
  usageTracker.forEach((usage, model) => {
    const modelConfig = config.models[model] || {};
    const budget = modelConfig.budget || 'N/A';
    const costPerToken = modelConfig.costPerToken || 0;
    lines.push(`- ${model}:`);
    lines.push(`  Tokens Used: ${usage.tokensUsed}`);
    lines.push(`  Cost Used: $${(usage.costUsed).toFixed(2)}`);
    lines.push(`  Budget: $${budget}`);
    lines.push(`  Cost per Token: $${costPerToken}`);
  });

  lines.push('');
  lines.push('Per-Model Budget Status:');
  usageTracker.forEach((usage, model) => {
    const modelConfig = config.models[model] || {};
    const budget = modelConfig.budget || 0;
    const remaining = budget - usage.costUsed;
    const status = remaining >= 0 ? 'OK' : 'OVER';
    lines.push(`- ${model}: ${status} (${remaining >= 0 ? `$${remaining.toFixed(2)} remaining` : `$${-remaining.toFixed(2)} over`})`);
  });

  lines.push('');
  lines.push('Sensitivity Limits (per request):');
  Object.entries(config.sensitivityLimits).forEach(([sensitivity, limit]) => {
    lines.push(`- ${sensitivity}: ${limit} tokens`);
  });

  return lines.join('\n');
}

module.exports = {
  checkBudget,
  checkTokenLimit,
  recordUsage,
  generateComplianceReport,
};