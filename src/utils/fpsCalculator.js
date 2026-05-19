function calculateFPSGain(currentConfig, targetGame, upgradeOptions) {
    const baseFPS = calculateBaseFPS(currentConfig, targetGame);
    return upgradeOptions.map(upgrade => ({
        ...upgrade,
        expectedFPS: calculateExpectedFPS(baseFPS, upgrade),
        fpsGain: calculateExpectedFPS(baseFPS, upgrade) - baseFPS,
        cost: upgrade.cost
    }));
}

function calculateBaseFPS(currentConfig, targetGame) {
    // Placeholder logic for calculating base FPS based on current hardware and game
    return 60; // Example value
}

function calculateExpectedFPS(baseFPS, upgrade) {
    // Placeholder logic for calculating expected FPS after applying an upgrade
    return baseFPS * (1 + upgrade.performanceBoost); // Example calculation
}

module.exports = {
    calculateFPSGain
};