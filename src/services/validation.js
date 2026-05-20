/**
 * Mock validation service for pipeline.yaml.
 *
 * In a real implementation this would call a backend or run a linter.
 * For the purposes of this feature we simply look for the string
 * "error" in the content and return a warning for each occurrence.
 *
 * @param {string} content - The YAML content to validate.
 * @returns {Promise<{errors: Array, warnings: Array}>}
 */
export async function validatePipeline(content) {
  // Simulate async validation delay
  await new Promise((resolve) => setTimeout(resolve, 200));

  const errors = [];
  const warnings = [];

  const lines = content.split('\n');
  lines.forEach((line, idx) => {
    const trimmed = line.trim();
    if (trimmed.startsWith('#')) return; // ignore comments

    if (trimmed.includes('error')) {
      errors.push({
        lineNumber: idx + 1,
        column: trimmed.indexOf('error') + 1,
        message: 'Found forbidden keyword "error".',
        severity: 'error',
      });
    } else if (trimmed.includes('warn')) {
      warnings.push({
        lineNumber: idx + 1,
        column: trimmed.indexOf('warn') + 1,
        message: 'Found keyword "warn".',
        severity: 'warning',
      });
    }
  });

  return { errors, warnings };
}