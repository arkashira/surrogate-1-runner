/**
 * Forecasting Settings Module
 *
 * Provides a strongly‑typed configuration object for the forecasting
 * algorithm and utilities to load/validate user‑provided settings.
 *
 * The settings can be supplied programmatically (e.g. from a UI or API)
 * or via environment variables for CI/CD / CLI usage.
 */

export type ForecastAlgorithm = 'linear' | 'exponential' | 'arima';

/**
 * Complete set of forecasting configuration options.
 */
export interface ForecastingSettings {
  /** Number of future days to predict. Must be > 0. */
  horizonDays: number;
  /** Desired confidence level for prediction intervals (0‑1). */
  confidenceLevel: number;
  /** Algorithm to use for forecasting. */
  algorithm: ForecastAlgorithm;
  /** Whether to include seasonal components in the model. */
  includeSeasonality: boolean;
}

/**
 * Default configuration values used when the user does not specify a setting.
 */
export const DEFAULT_FORECASTING_SETTINGS: ForecastingSettings = {
  horizonDays: 30,
  confidenceLevel: 0.95,
  algorithm: 'linear',
  includeSeasonality: false,
};

/**
 * Validate a partial or full settings object.
 * Throws an Error if any field is invalid.
 */
export function validateSettings(settings: Partial<ForecastingSettings>): void {
  if (settings.horizonDays !== undefined) {
    if (!Number.isInteger(settings.horizonDays) || settings.horizonDays <= 0) {
      throw new Error('horizonDays must be a positive integer');
    }
  }

  if (settings.confidenceLevel !== undefined) {
    if (
      typeof settings.confidenceLevel !== 'number' ||
      settings.confidenceLevel <= 0 ||
      settings.confidenceLevel >= 1
    ) {
      throw new Error('confidenceLevel must be a number between 0 and 1 (exclusive)');
    }
  }

  if (settings.algorithm !== undefined) {
    const allowed: ForecastAlgorithm[] = ['linear', 'exponential', 'arima'];
    if (!allowed.includes(settings.algorithm as ForecastAlgorithm)) {
      throw new Error(`algorithm must be one of ${allowed.join(', ')}`);
    }
  }

  if (settings.includeSeasonality !== undefined) {
    if (typeof settings.includeSeasonality !== 'boolean') {
      throw new Error('includeSeasonality must be a boolean');
    }
  }
}

/**
 * Merge user‑provided partial settings with defaults, performing validation.
 *
 * @param overrides Partial settings supplied by the user or caller.
 * @returns A fully‑populated, validated ForecastingSettings object.
 */
export function loadForecastingSettings(
  overrides: Partial<ForecastingSettings> = {}
): ForecastingSettings {
  // Validate before merging so we can give precise error messages.
  validateSettings(overrides);

  return {
    ...DEFAULT_FORECASTING_SETTINGS,
    ...overrides,
  };
}

/**
 * Service that reads configuration from environment variables.
 *
 * Environment variables:
 *   FORECAST_HORIZON_DAYS          (integer)
 *   FORECAST_CONFIDENCE_LEVEL     (float 0‑1)
 *   FORECAST_ALGORITHM            (linear|exponential|arima)
 *   FORECAST_INCLUDE_SEASONALITY  (true|false)
 *
 * If a variable is missing, the default value is used.
 */
export class ForecastingConfigService {
  /**
   * Load settings from the process environment.
   *
   * @returns Fully‑validated ForecastingSettings.
   */
  static fromEnv(): ForecastingSettings {
    const env = process.env;

    const overrides: Partial<ForecastingSettings> = {};

    if (env.FORECAST_HORIZON_DAYS !== undefined) {
      const parsed = parseInt(env.FORECAST_HORIZON_DAYS, 10);
      if (!Number.isNaN(parsed)) {
        overrides.horizonDays = parsed;
      }
    }

    if (env.FORECAST_CONFIDENCE_LEVEL !== undefined) {
      const parsed = parseFloat(env.FORECAST_CONFIDENCE_LEVEL);
      if (!Number.isNaN(parsed)) {
        overrides.confidenceLevel = parsed;
      }
    }

    if (env.FORECAST_ALGORITHM !== undefined) {
      overrides.algorithm = env.FORECAST_ALGORITHM as ForecastAlgorithm;
    }

    if (env.FORECAST_INCLUDE_SEASONALITY !== undefined) {
      const val = env.FORECAST_INCLUDE_SEASONALITY.toLowerCase();
      overrides.includeSeasonality = val === 'true' || val === '1';
    }

    return loadForecastingSettings(overrides);
  }
}