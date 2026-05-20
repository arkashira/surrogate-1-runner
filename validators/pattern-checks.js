const { logger } = require('../utils/logger');
const { loadK8sVersions } = require('../data/k8s-versions');
const { Pattern } = require('../models/pattern');

/**
 * Validates a pattern against a given Kubernetes version and application type.
 * @param {Pattern} pattern - The pattern object to validate.
 * @param {string} k8sVersion - The Kubernetes version to check against.
 * @param {string} appType - The application type (e.g., 'web', 'microservices').
 * @returns {Object} Validation result with status, compatibility, and filtered patterns.
 */
function validatePattern(pattern, k8sVersion, appType) {
  try {
    const k8sVersions = loadK8sVersions();
    const currentVersion = k8sVersions.find(v => v.version === k8sVersion);

    if (!currentVersion) {
      logger.warn(`Kubernetes version ${k8sVersion} not found in database.`);
      return {
        status: 'error',
        message: `Unsupported Kubernetes version: ${k8sVersion}`,
        compatible: false,
        filteredPatterns: []
      };
    }

    const isCompatible = checkK8sCompatibility(pattern, currentVersion);
    const filteredPatterns = filterByAppType(patterns, appType);

    return {
      status: 'success',
      message: 'Pattern validated successfully.',
      compatible: isCompatible,
      filteredPatterns: filteredPatterns,
      votes: pattern.votes || 0
    };
  } catch (error) {
    logger.error('Pattern validation failed:', error);
    return {
      status: 'error',
      message: error.message,
      compatible: false,
      filteredPatterns: []
    };
  }
}

/**
 * Checks if a pattern is compatible with a given Kubernetes version.
 * @param {Pattern} pattern - The pattern object.
 * @param {Object} k8sVersion - The Kubernetes version object.
 * @returns {boolean} True if compatible, false otherwise.
 */
function checkK8sCompatibility(pattern, k8sVersion) {
  if (!pattern.kubernetes) {
    logger.warn('Pattern does not specify Kubernetes requirements.');
    return false;
  }

  const { minVersion, maxVersion } = pattern.kubernetes;

  const currentMajor = k8sVersion.major;
  const currentMinor = k8sVersion.minor;

  if (minVersion && (currentMajor < minVersion || (currentMajor === minVersion && currentMinor < minVersion))) {
    return false;
  }

  if (maxVersion && (currentMajor > maxVersion || (currentMajor === maxVersion && currentMinor > maxVersion))) {
    return false;
  }

  return true;
}

/**
 * Filters patterns by application type.
 * @param {Array<Pattern>} patterns - List of patterns.
 * @param {string} appType - The application type to filter by.
 * @returns {Array<Pattern>} Filtered patterns.
 */
function filterByAppType(patterns, appType) {
  if (!appType) {
    return patterns;
  }

  return patterns.filter(pattern => pattern.appType === appType);
}

module.exports = {
  validatePattern,
  checkK8sCompatibility,
  filterByAppType
};