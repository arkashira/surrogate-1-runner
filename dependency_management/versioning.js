const fs = require('fs').promises;
const path = require('path');

/**
 * Central dependency registry file.
 * Stored at the project root for easy access and version control.
 */
const DEP_FILE = path.resolve(__dirname, '..', '..', 'dependencies.json');

/**
 * Load dependencies from the central JSON file.
 * If the file does not exist, an empty object is returned.
 * @returns {Promise<Object<string, string>>} Map of dependency name to version.
 */
async function loadDependencies() {
  try {
    const data = await fs.readFile(DEP_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') {
      // File missing – start with an empty registry
      return {};
    }
    throw err;
  }
}

/**
 * Persist the dependency map to the central JSON file.
 * @param {Object<string, string>} deps
 * @returns {Promise<void>}
 */
async function saveDependencies(deps) {
  const data = JSON.stringify(deps, null, 2);
  await fs.writeFile(DEP_FILE, data, 'utf8');
}

/**
 * Add a new dependency to the registry.
 * Throws if the dependency already exists.
 * @param {string} name
 * @param {string} version
 * @returns {Promise<void>}
 */
async function addDependency(name, version) {
  const deps = await loadDependencies();
  if (deps[name]) {
    throw new Error(`Dependency "${name}" already exists with version ${deps[name]}`);
  }
  deps[name] = version;
  await saveDependencies(deps);
}

/**
 * Remove an existing dependency from the registry.
 * Throws if the dependency does not exist.
 * @param {string} name
 * @returns {Promise<void>}
 */
async function removeDependency(name) {
  const deps = await loadDependencies();
  if (!deps[name]) {
    throw new Error(`Dependency "${name}" not found`);
  }
  delete deps[name];
  await saveDependencies(deps);
}

/**
 * Update the version of an existing dependency.
 * Throws if the dependency does not exist.
 * @param {string} name
 * @param {string} newVersion
 * @returns {Promise<void>}
 */
async function updateDependency(name, newVersion) {
  const deps = await loadDependencies();
  if (!deps[name]) {
    throw new Error(`Dependency "${name}" not found`);
  }
  deps[name] = newVersion;
  await saveDependencies(deps);
}

/**
 * Retrieve all dependencies as an array of objects.
 * @returns {Promise<Array<{name: string, version: string}>>}
 */
async function getDependencies() {
  const deps = await loadDependencies();
  return Object.entries(deps).map(([name, version]) => ({ name, version }));
}

/**
 * Retrieve the version of a specific dependency.
 * @param {string} name
 * @returns {Promise<string|null>} Version string or null if not found.
 */
async function getDependency(name) {
  const deps = await loadDependencies();
  return deps[name] ?? null;
}

module.exports = {
  addDependency,
  removeDependency,
  updateDependency,
  getDependencies,
  getDependency,
  // Exported for testing purposes
  _loadDependencies: loadDependencies,
  _saveDependencies: saveDependencies,
  _DEP_FILE: DEP_FILE,
};