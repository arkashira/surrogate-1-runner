export interface ForecastingConfig {
    period: number;
    method: string;
}

export function loadForecastingConfig(): ForecastingConfig {
    // Load configuration from a file or environment variables
    return {
        period: parseInt(process.env.FORECAST_PERIOD || '3', 10),
        method: process.env.FORECAST_METHOD || 'simple-moving-average'
    };
}

export function saveForecastingConfig(config: ForecastingConfig): void {
    // Save configuration to a file or environment variables
    process.env.FORECAST_PERIOD = config.period.toString();
    process.env.FORECAST_METHOD = config.method;
}