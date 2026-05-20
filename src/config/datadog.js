/**
 * Datadog configuration loader.
 *
 * Reads environment variables:
 *   - DATADOG_SANDBOX_MODE  : string, defaults to "production"
 *   - DATADOG_ERROR_RATE    : float, defaults to 0.0
 *
 * @throws {Error} If DATADOG_ERROR_RATE is present but not a valid number,
 *                 or if it falls outside the inclusive range [0, 1].
 * @returns {{ sandboxMode: string, errorRate: number }}
 */
const getDatadogConfig = () => {
  // Grab raw env values
  const rawMode = process.env.DATADOG_SANDBOX_MODE;
  const rawErrorRate = process.env.DATADOG_ERROR_RATE;

  // ---- sandboxMode ---------------------------------------------------------
  // Default to "production". Trim whitespace so " sandbox " → "sandbox".
  const sandboxMode = rawMode !== undefined ? String(rawMode).trim() : 'production';

  // ---- errorRate ------------------------------------------------------------
  let errorRate = 0.0; // default

  if (rawErrorRate !== undefined) {
    const parsed = parseFloat(rawErrorRate);
    if (Number.isNaN(parsed)) {
      throw new Error(
        `Invalid DATADOG_ERROR_RATE: "${rawErrorRate}". Must be a numeric value.`
      );
    }
    if (parsed < 0 || parsed > 1) {
      throw new Error(
        `DATADOG_ERROR_RATE out of range: ${parsed}. Expected a value between 0 and 1.`
      );
    }
    errorRate = parsed;
  }

  return { sandboxMode, errorRate };
};

module.exports = { getDatadogConfig };