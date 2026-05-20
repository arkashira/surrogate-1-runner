const { logger } = require('../utils/logger');

class DependencyValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'DependencyValidationError';
  }
}

class ErrorHandler {
  static handleValidationError(error) {
    logger.error(`Dependency validation failed: ${error.message}`);
    throw new DependencyValidationError(error.message);
  }

  static handleUnexpectedError(error) {
    logger.error(`Unexpected error during validation: ${error.message}`);
    throw new Error(`Validation process failed: ${error.message}`);
  }
}

module.exports = { ErrorHandler, DependencyValidationError };