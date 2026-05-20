/**
 * Datadog Sandbox Configuration
 * 
 * Loads environment variables to parameterize sandbox behavior for CI/CD tests.
 * 
 * Supported Env Vars:
 * - DATADOG_SANDBOX_MODE: (string) 'true' | 'false' | undefined. Defaults to 'false'.
 * - DATADOG_ERROR_RATE: (number) 0.0 to 1.0. Defaults to 0.0.
 * 
 * The configuration object is frozen to prevent runtime mutations.
 */

function parseBool(val) {
  if (typeof val === 'string') {
    const trimmed = val.trim().toLowerCase();
    return trimmed === 'true';
  }
  return false;
}

function parseErrorRate(val, defaultValue = 0.0) {
  const num = Number(val);
  // Validate: must be finite, within range [0, 1], and not NaN
  if (Number.isFinite(num) && num >= 0 && num <= 1) {
    return num;
  }
  return defaultValue;
}

const config = {
  /**
   * Indicates if the application is running in a Datadog sandbox mode.
   * Useful for bypassing real telemetry or simulating specific environments.
   */
  sandboxMode: parseBool(process.env.DATADOG_SANDBOX_MODE),

  /**
   * Simulated error rate for testing error handling logic.
   * Value should be between 0.0 and 1.0.
   */
  errorRate: parseErrorRate(process.env.DATADOG_ERROR_RATE),
};

// Freeze the config to prevent runtime mutations
module.exports = Object.freeze(config);