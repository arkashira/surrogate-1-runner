/**
 * Surrogate‑1 orchestrator
 *
 * Loads configuration, registers providers, and aggregates data.
 * Each provider must expose a `collectResources()` method that returns
 * a Promise resolving to a normalised object.
 */

const path = require("path");
const fs = require("fs");

// ------------------------------------------------------------------
// Load configuration
// ------------------------------------------------------------------
const configPath = path.resolve(__dirname, "config.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));

// ------------------------------------------------------------------
// Provider registry
// ------------------------------------------------------------------
const providers = [];

// AWS provider (existing)
if (config.aws?.accessKeyId) {
  const AWSProvider = require("./providers/aws");
  providers.push(new AWSProvider(config.aws));
}

// Azure provider (new)
if (config.azure?.subscriptionId) {
  const AzureProvider = require("./providers/azure");
  providers.push(new AzureProvider(config.azure));
}

// GCP provider (existing)
if (config.gcp?.projectId) {
  const GCPProvider = require("./providers/gcp");
  providers.push(new GCPProvider(config.gcp));
}

// Private cloud provider (existing)
if (config.private?.endpoint) {
  const PrivateProvider = require("./providers/private");
  providers.push(new PrivateProvider(config.private));
}

// ------------------------------------------------------------------
// Data collection
// ------------------------------------------------------------------
async function collectAll() {
  const results = [];
  for (const provider of providers) {
    try {
      const data = await provider.collectResources();
      results.push(data);
    } catch (err) {
      console.error(
        `Error collecting from ${provider.constructor.name}:`,
        err.message
      );
    }
  }
  return results;
}

module.exports = { collectAll };