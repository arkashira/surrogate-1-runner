const { calculateFPSGain } = require('./fpsCalculator');

describe('calculateFPSGain', () => {
    const currentConfig = {}; // Placeholder for current hardware config
    const targetGame = {}; // Placeholder for target game details
    const upgradeOptions = [
        { performanceBoost: 0.1, cost: 100 },
        { performanceBoost: 0.2, cost: 200 }
    ];

    it('should calculate expected FPS gains and costs for each upgrade option', () => {
        const results = calculateFPSGain(currentConfig, targetGame, upgradeOptions);
        expect(results).toEqual([
            { performanceBoost: 0.1, cost: 100, expectedFPS: 66, fpsGain: 6 },
            { performanceBoost: 0.2, cost: 200, expectedFPS: 72, fpsGain: 12 }
        ]);
    });
});