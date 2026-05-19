// Combined AI Proposal

// /opt/axentx/surrogate-1/core/orchestration/tools.js
/**
 * Subagent orchestration utilities.
 *
 * This module provides a simple and lightweight API to manage subagents.
 * Subagents are persisted in a JSON configuration file (`agent-config.json`)
 * located in the same directory as this module. Each subagent is represented
 * by a unique name and an optional configuration object.
 *
 * The API supports adding, removing, configuring, and communicating between
 * subagents. For more advanced use cases (e.g., distributed agents), the
 * communication layer can be extended to use message queues or HTTP endpoints.
 */

const fs = require('fs');
const path = require('path');
const EventEmitter = require('events');

const CONFIG_FILE = path.resolve(__dirname, 'agent-config.json');

/**
 * Load the current agent configuration from disk.
 * @returns {Object} The parsed JSON configuration.
 */
function loadConfig() {
  try {
    const data = fs.readFileSync(CONFIG_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    // If file does not exist, start with an empty config.
    if (err.code === 'ENOENT') {
      return { subagents: {} };
    }
    throw err;
  }
}

/**
 * Persist the given configuration to disk.
 * @param {Object} config The configuration object to write.
 */
function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf8');
}

/**
 * Registry holds subagent definitions keyed by a unique name.
 * Each entry contains:
 *   - instance: the actual subagent object (could be a class instance)
 *   - config: configuration object passed to the subagent
 */
const registry = new Map();

/**
 * Event bus for inter-subagent communication.
 * Subagents can listen for messages addressed to them or broadcast.
 */
const bus = new EventEmitter();

/**
 * Add a new subagent to the registry.
 *
 * @param {string} name - Unique identifier for the subagent.
 * @param {object} instance - The subagent instance (must have a `handleMessage` method).
 * @param {object} [config={}] - Optional configuration for the subagent.
 * @throws {Error} if the name is already in use or instance lacks handler.
 */
function addSubagent(name, instance, config = {}) {
  if (registry.has(name)) {
    throw new Error(`Subagent with name "${name}" already exists`);
  }
  if (typeof instance.handleMessage !== 'function') {
    throw new Error('Subagent instance must implement handleMessage(message)');
  }
  registry.set(name, { instance, config });

  // Subscribe the subagent to the bus
  bus.on(name, (msg) => instance.handleMessage(msg));
}

/**
 * Remove a subagent from the registry.
 *
 * @param {string} name - Name of the subagent to remove.
 * @throws {Error} if the subagent does not exist.
 */
function removeSubagent(name) {
  if (!registry.has(name)) {
    throw new Error(`Subagent "${name}" not found`);
  }
  const { instance } = registry.get(name);
  bus.removeAllListeners(name);
  registry.delete(name);
  // If the instance has a cleanup method, call it.
  if (typeof instance.cleanup === 'function') {
    instance.cleanup();
  }
}

/**
 * Retrieve the configuration of a subagent.
 *
 * @param {string} name - Subagent name.
 * @returns {object} configuration object.
 * @throws {Error} if the subagent does not exist.
 */
function getSubagentConfig(name) {
  const entry = registry.get(name);
  if (!entry) throw new Error(`Subagent "${name}" not found`);
  return entry.config;
}

/**
 * Update the configuration of an existing subagent.
 *
 * @param {string} name - Subagent name.
 * @param {object} newConfig - New configuration object.
 * @throws {Error} if the subagent does not exist.
 */
function setSubagentConfig(name, newConfig) {
  const entry = registry.get(name);
  if (!entry) throw new Error(`Subagent "${name}" not found`);
  entry.config = { ...entry.config, ...newConfig };
  // Notify the subagent of the new config if it supports it.
  if (typeof entry.instance.onConfigChange === 'function') {
    entry.instance.onConfigChange(entry.config);
  }
}

/**
 * List all registered subagents.
 *
 * @returns {Array<string>} array of subagent names.
 */
function listSubagents() {
  return Array.from(registry.keys());
}

/**
 * Load the subagent registry from the configuration file.
 */
function loadRegistry() {
  const config = loadConfig();
  for (const name in config.subagents) {
    const instance = new config.subagents[name].constructor(config.subagents[name].args);
    addSubagent(name, instance, config.subagents[name].config);
  }
}

/**
 * Save the subagent registry to the configuration file.
 */
function saveRegistry() {
  const subagents = Array.from(registry.values()).map(({ instance, config }) => ({
    constructor: instance.constructor.name,
    args: instance.constructor.args,
    config,
  }));
  saveConfig({ subagents });
}

/**
 * Send a message to a specific subagent or broadcast to all.
 *
 * @param {string} target - Subagent name or '*' for broadcast.
 * @param {object} message - Payload to send.
 */
function sendMessage(target, message) {
  if (target === '*') {
    // Broadcast to all subagents
    for (const name of registry.keys()) {
      bus.emit(name, message);
    }
  } else {
    if (!registry.has(target)) {
      throw new Error(`Target subagent "${target}" not found`);
    }
    bus.emit(target, message);
  }
}

/**
 * Exported API.
 */
module.exports = {
  loadRegistry,
  saveRegistry,
  addSubagent,
  removeSubagent,
  getSubagentConfig,
  setSubagentConfig,
  listSubagents,
  sendMessage,
  _bus: bus,
};