const IRSRulesService = require('./irsRules');

describe('IRSRulesService', () => {
    let irsRulesService;

    beforeEach(() => {
        irsRulesService = new IRSRulesService();
    });

    test('should get correct tax bracket', () => {
        expect(irsRulesService.getTaxBracket(5000)).toBe('10%');
        expect(irsRulesService.getTaxBracket(30000)).toBe('12%');
    });

    test('should calculate tax impact correctly', () => {
        const result = irsRulesService.calculateTaxImpact(10000, 5000, '12%');
        expect(result.taxSavingsLosses).toBeCloseTo(600);
        expect(result.adjustedBasis).toBe(15000);
        expect(result.recharacterizationImpact).toBeCloseTo(1800);
    });
});