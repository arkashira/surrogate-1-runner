function validateHardwareInput(input) {
  const requiredFields = ['cpu', 'gpu', 'ram', 'storage', 'motherboard'];
  const errors = [];

  requiredFields.forEach((field) => {
    if (!input[field] || input[field].trim() === '') {
      errors.push(`${field} is required`);
    }
  });

  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }

  return input;
}

module.exports = validateHardwareInput;