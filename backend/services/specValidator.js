function validateSpec(spec) {
  // Implement spec validation logic
  // This is a placeholder for the real implementation
  const errors = [];

  if (!spec || typeof spec !== 'object') {
    errors.push('Spec must be a non-null object');
  }

  // Add more validation rules as needed

  return {
    valid: errors.length === 0,
    errors: errors
  };
}

module.exports = { validateSpec };