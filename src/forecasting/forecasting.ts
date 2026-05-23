export class CostForecasting {
    private historicalData: number[];
    private config: { period: number; method: string };

    constructor(historicalData: number[], config: { period: number; method: string }) {
        this.historicalData = historicalData;
        this.config = config;
    }

    public setConfig(config: { period: number; method: string }): void {
        this.config = config;
    }

    private simpleMovingAverage(): number[] {
        const period = this.config.period;
        const averages: number[] = [];
        for (let i = period; i < this.historicalData.length; i++) {
            const sum = this.historicalData.slice(i - period, i).reduce((acc, val) => acc + val, 0);
            averages.push(sum / period);
        }
        return averages;
    }

    public forecast(): number[] {
        switch (this.config.method) {
            case 'simple-moving-average':
                return this.simpleMovingAverage();
            default:
                throw new Error('Unsupported forecasting method');
        }
    }
}

// Example usage:
// const forecasting = new CostForecasting([100, 150, 200, 250, 300], { period: 3, method: 'simple-moving-average' });
// console.log(forecasting.forecast());