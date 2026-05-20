/**
 * Validation utilities for build recommendation inputs
 */
class InputValidator {
  /**
   * Validate budget input
   * @param {number} budget - User's budget
   * @returns {boolean} - Whether validation passes
   */
  static validateBudget(budget) {
    if (typeof budget !== 'number' || isNaN(budget)) {
      return false;
    }
    if (budget < 0) {
      return false;
    }
    if (budget > 1000000) { // $1M max budget
      return false;
    }
    return true;
  }

  /**
   * Validate build requirements
   * @param {string} requirements - User's requirements text
   * @returns {boolean} - Whether validation passes
   */
  static validateRequirements(requirements) {
    if (!requirements || typeof requirements !== 'string') {
      return false;
    }
    if (requirements.trim().length < 10) {
      return false;
    }
    return true;
  }

  /**
   * Validate all inputs
   * @param {Object} inputs - User inputs
   * @returns {Object} - Validation results
   */
  static validateAll(inputs) {
    const results = {
      budget: this.validateBudget(inputs.budget),
      requirements: this.validateRequirements(inputs.requirements),
      budgetError: '',
      requirementsError: ''
    };

    if (!results.budget) {
      results.budgetError = 'Budget must be a positive number';
    }
    if (!results.requirements) {
      results.requirementsError = 'Please provide detailed build requirements';
    }

    return results;
  }
}

export default InputValidator;