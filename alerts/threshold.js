const monthlyCostThreshold = 1000;

module.exports = {
  shouldSendAlert: (monthlyCost) => {
    return monthlyCost > monthlyCostThreshold;
  }
};