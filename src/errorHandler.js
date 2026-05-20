const logger = require('./logger');

function handleVerificationError(error, moduleName) {
    logger.error(`Verification error in ${moduleName}: ${error.message}`);
    const errorMessage = `Dependency inconsistency detected in ${moduleName}. Please check your package.json and import statements.`;
    console.error(errorMessage);
    throw new Error(errorMessage);
}

module.exports = {
    handleVerificationError
};