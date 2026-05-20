class IRSRulesService {
    constructor() {
        this.rules = this.loadIRSRuleData();
    }

    loadIRSRuleData() {
        // Placeholder for loading IRS rule data from an internal rule set.
        // This should be replaced with actual implementation.
        return [
            { year: 2023, taxBracket: '10%', maxIncome: 10000 },
            { year: 2023, taxBracket: '12%', maxIncome: 40000 },
            // Add more rules as needed.
        ];
    }

    getTaxBracket(income) {
        const applicableRules = this.rules.filter(rule => income <= rule.maxIncome);
        return applicableRules.length > 0 ? applicableRules[applicableRules.length - 1].taxBracket : 'Unknown';
    }

    calculateTaxImpact(contributionAmount, conversionAmount, currentTaxBracket) {
        const taxSavingsLosses = conversionAmount * parseFloat(currentTaxBracket.replace('%', '')) / 100;
        const adjustedBasis = contributionAmount + conversionAmount;
        const recharacterizationImpact = adjustedBasis * parseFloat(currentTaxBracket.replace('%', '')) / 100;

        return {
            taxSavingsLosses,
            adjustedBasis,
            recharacterizationImpact
        };
    }
}

module.exports = IRSRulesService;