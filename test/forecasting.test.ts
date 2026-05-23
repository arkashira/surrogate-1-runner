import { ForecastService } from '../src/forecasting/forecastService';
import { loadForecastingConfig } from '../src/forecasting/config';

describe('Forecasting Algorithm', () => {
    let service: ForecastService;

    beforeEach(() => {
        const historicalData = [100, 150, 200, 250, 300];
        service = new ForecastService(historicalData);
    });

    it('should forecast future costs using simple moving average', () => {
        const config = loadForecastingConfig();
        config.method = 'simple-moving-average';
        config.period = 3;
        service.setForecastingConfig(config);

        const forecast = service.getForecast();
        expect(forecast).toEqual([183.33333333333334, 233.33333333333334]);
    });
});