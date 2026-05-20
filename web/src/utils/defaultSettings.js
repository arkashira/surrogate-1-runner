/**
 * Default settings for surrogate-1 instance setup wizard
 * @returns {Object} Default configuration values
 */
export const getDefaultSettings = () => ({
  // Step 1: Select model - defaults to first available model
  model: 'surrogate-1-base',
  
  // Step 2: Set data size - defaults to 1000 records
  dataSize: 1000,
  
  // Step 3: Confirm - no additional defaults needed
  // Additional settings that apply across all steps
  batchSize: 32,
  epochs: 5,
  learningRate: 0.001
});

/**
 * Validates if provided settings contain all required fields
 * @param {Object} settings - Settings object to validate
 * @returns {boolean} True if settings are valid
 */
export const validateSettings = (settings) => {
  if (!settings) return false;
  return (
    typeof settings.model === 'string' &&
    settings.model.length > 0 &&
    typeof settings.dataSize === 'number' &&
    settings.dataSize > 0 &&
    settings.dataSize <= 1000000 // Reasonable upper limit
  );
};

/**
 * Applies default settings to partial settings object
 * @param {Object} partialSettings - User-provided settings (may be incomplete)
 * @returns {Object} Complete settings with defaults applied
 */
export const applyDefaults = (partialSettings = {}) => {
  const defaults = getDefaultSettings();
  return {
    ...defaults,
    ...partialSettings,
    // Ensure dataSize is always a number
    dataSize: Number(partialSettings.dataSize) || defaults.dataSize
  };
};