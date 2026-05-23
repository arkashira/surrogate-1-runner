import { CostForecasting } from './forecasting';
import { loadForecastingConfig, saveForecastingConfig } from './config';

export class ForecastService {
    private forecasting: CostForecasting;

    constructor(historicalData: number[]) {
        const config = loadForecastingConfig();
        this.forecasting = new CostForecasting(historicalData, config);
    }

    public setForecastingConfig(config: ForecastingConfig): void {
        saveForecastingConfig(config);
        this.forecasting.setConfig(config);
    }

    public getForecast(): number[] {
        return this.forecasting.forecast();
    }
}