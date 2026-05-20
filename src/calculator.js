const ruleUpdater = require('./services/ruleUpdater');

async function calculateTaxes(income) {
  const rules = await ruleUpdater.getLatestRules();
  if (!rules) {
    console.error('No rules available for calculation.');
    return null;
  }

  // Example calculation based on fetched rules
  const taxRate = rules.tax_brackets.find(bracket => income >= bracket.min && income <= bracket.max)?.rate || 0;
  return income * taxRate;
}

module.exports = {
  calculateTaxes
};