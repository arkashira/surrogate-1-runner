const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.resolve(__dirname, '..', 'config.json');

function loadConfig() {
  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch (_) {
    // Return empty config if file does not exist or is malformed
    return {};
  }
}

function saveConfig(config) {
  const data = JSON.stringify(config, null, 2);
  fs.writeFileSync(CONFIG_PATH, data, { mode: 0o600 });
}

/**
 * Retrieves the integration configuration.
 * Returns an object with `endpoint`, `username`, and `password` fields.
 * If not set, returns an empty object.
 */
function getIntegrationConfig() {
  const cfg = loadConfig();
  return cfg.integration || {};
}

/**
 * Persists the integration configuration.
 * @param {{endpoint:string, username:string, password:string}} newConfig
 */
function setIntegrationConfig(newConfig) {
  const cfg = loadConfig();
  cfg.integration = {
    endpoint: newConfig.endpoint,
    username: newConfig.username,
    // Store password securely – in a real system this would be encrypted or
    // delegated to a secret manager. For this prototype we keep it plain but
    // restrict file permissions via `saveConfig`.
    password: newConfig.password,
  };
  saveConfig(cfg);
}

module.exports = {
  getIntegrationConfig,
  setIntegrationConfig,
};