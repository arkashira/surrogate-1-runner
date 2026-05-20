const axios = require('axios');
const { validateAgainstRegulatoryRequirements } = require('../utils/regulatory-utils');

class PolicyValidation {
  constructor(policy) {
    this.policy = policy;
  }

  async validateLocally() {
    const validationResult = validateAgainstRegulatoryRequirements(this.policy);
    return {
      isValid: validationResult.isValid,
      errors: validationResult.errors,
      warnings: validationResult.warnings
    };
  }

  async validateExternally(apiUrl = 'https://regulatory-api.com/validate') {
    try {
      const response = await axios.get(`${apiUrl}/${this.policy.id}`);
      return response.data.valid;
    } catch (error) {
      console.error(`External validation failed for policy ${this.policy.id}:`, error.message);
      throw new Error('External validation service unavailable');
    }
  }

  async validate() {
    // First perform local validation
    const localResult = await this.validateLocally();

    if (!localResult.isValid) {
      return {
        isValid: false,
        errors: localResult.errors,
        warnings: localResult.warnings
      };
    }

    // Then attempt external validation if needed
    try {
      const externalValid = await this.validateExternally();
      return {
        isValid: externalValid,
        errors: [],
        warnings: []
      };
    } catch (err) {
      // If external validation fails, still return local results but log the issue
      console.warn(`Fallback to local validation due to external failure: ${err.message}`);
      return localResult;
    }
  }
}

module.exports = PolicyValidation;