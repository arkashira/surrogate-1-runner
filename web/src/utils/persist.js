/**
 * Utility for persisting wizard state to a temporary JSON file.
 *
 * The wizard can be aborted and later resumed without losing prior inputs.
 * State is stored in the OS temporary directory under a deterministic filename.
 *
 * Exported API:
 *   - saveState(state: object): Promise<void>
 *   - loadState(): Promise<object|null>
 *   - clearState(): Promise<void>
 *
 * The functions are safe to call multiple times and handle missing files
 * gracefully.
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');

const STATE_FILENAME = 'surrogate-wizard-state.json';

/**
 * Returns the absolute path to the temporary state file.
 * The file lives in the OS temp directory to avoid polluting the project.
 */
function getStateFilePath() {
  return path.join(os.tmpdir(), STATE_FILENAME);
}

/**
 * Persists the given state object as JSON.
 *
 * @param {object} state - Arbitrary serializable wizard state.
 * @returns {Promise<void>}
 */
async function saveState(state) {
  if (typeof state !== 'object' || state === null) {
    throw new TypeError('State must be a non‑null object');
  }
  const filePath = getStateFilePath();
  const data = JSON.stringify(state, null, 2);
  await fs.writeFile(filePath, data, { encoding: 'utf8' });
}

/**
 * Loads the persisted wizard state.
 *
 * @returns {Promise<object|null>} Returns the state object or null if no state exists.
 */
async function loadState() {
  const filePath = getStateFilePath();
  try {
    const data = await fs.readFile(filePath, { encoding: 'utf8' });
    return JSON.parse(data);
  } catch (err) {
    // If the file does not exist, treat it as no saved state.
    if (err.code === 'ENOENT') {
      return null;
    }
    // Propagate other errors.
    throw err;
  }
}

/**
 * Removes the persisted state file.
 *
 * @returns {Promise<void>}
 */
async function clearState() {
  const filePath = getStateFilePath();
  try {
    await fs.unlink(filePath);
  } catch (err) {
    // Ignore if the file is already missing.
    if (err.code !== 'ENOENT') {
      throw err;
    }
  }
}

module.exports = {
  saveState,
  loadState,
  clearState,
  // Exported for testing / debugging purposes.
  _internal: {
    getStateFilePath,
    STATE_FILENAME,
  },
};