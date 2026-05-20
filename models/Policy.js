class Policy {
  constructor(modelCostBudget, alertThreshold, tokenUsageLimit) {
    this.modelCostBudget = modelCostBudget;
    this.alertThreshold = alertThreshold;
    this.tokenUsageLimit = tokenUsageLimit;
  }

  static async create(policyData) {
    // Simulate database interaction
    const policy = new Policy(
      policyData.modelCostBudget,
      policyData.alertThreshold,
      policyData.tokenUsageLimit
    );
    // Save policy to database
    console.log('Policy created:', policy);
    return policy;
  }

  static async get() {
    // Simulate fetching policy from database
    const policy = new Policy(1000, 800, 5000);
    console.log('Policy fetched:', policy);
    return policy;
  }
}

module.exports = Policy;