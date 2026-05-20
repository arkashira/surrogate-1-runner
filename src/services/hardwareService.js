const validateHardwareInput = require('./utils/validation');

function validateHardwareInputs(inputs) {
  try {
    const validatedInputs = validateHardwareInput(inputs);
    return validatedInputs;
  } catch (error) {
    throw error;
  }
}

module.exports = validateHardwareInputs;