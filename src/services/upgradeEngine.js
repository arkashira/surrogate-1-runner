const upgradeData = require('../data/upgradeData.json');

const calculateROI = (fpsGain, cost) => fpsGain / cost;

const getUpgradeCombinations = (budget, targetGame) => {
  const gameData = upgradeData[targetGame];
  const allCombinations = [];

  const generateCombinations = (remainingBudget, currentCombination) => {
    if (remainingBudget === 0) {
      allCombinations.push(currentCombination);
      return;
    }

    for (const [component, cost] of Object.entries(gameData.components)) {
      if (remainingBudget >= cost) {
        generateCombinations(remainingBudget - cost, [...currentCombination, component]);
      }
    }
  };

  generateCombinations(budget, []);

  return allCombinations;
};

const getTopUpgradeCombinations = (budget, targetGame) => {
  const combinations = getUpgradeCombinations(budget, targetGame);
  const rankedCombinations = combinations.sort((a, b) => {
    const fpsGainA = a.reduce((sum, component) => sum + gameData.components[component].fpsGain, 0);
    const fpsGainB = b.reduce((sum, component) => sum + gameData.components[component].fpsGain, 0);
    return calculateROI(fpsGainB, b.reduce((sum, component) => sum + gameData.components[component].cost, 0)) -
           calculateROI(fpsGainA, a.reduce((sum, component) => sum + gameData.components[component].cost, 0));
  });

  return rankedCombinations.slice(0, 3);
};

// /opt/axentx/surrogate-1/src/data/upgradeData.json
{
  "gameA": {
    "components": {
      "gpu1": { "cost": 300, "fpsGain": 30 },
      "gpu2": { "cost": 500, "fpsGain": 50 },
      "cpu1": { "cost": 200, "fpsGain": 20 },
      "cpu2": { "cost": 400, "fpsGain": 40 },
      "ram1": { "cost": 100, "fpsGain": 10 },
      "ram2": { "cost": 200, "fpsGain": 20 }
    }
  },
  "gameB": {
    // ... other games' data
  }
}