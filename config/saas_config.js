/**
 * Centralised configuration for the SaaS connector.
 * All values are sourced from environment variables so that secrets are never committed.
 */
const DEFAULTS = {
  apiKey: 'default-api-key',
  baseUrl: 'https://api.saas.example.com',
  encryptionKey: 'default-encryption-key', // 32‑byte key for AES‑256‑CBC
  supportedSaaS: ['shopify', 'hubspot', 'salesforce', 'zendesk'],
};

module.exports = {
  apiKey: process.env.SAAS_API_KEY || DEFAULTS.apiKey,
  baseUrl: process.env.SAAS_BASE_URL || DEFAULTS.baseUrl,
  encryptionKey: process.env.ENCRYPTION_KEY
    ? Buffer.from(process.env.ENCRYPTION_KEY, 'hex')
    : Buffer.from(DEFAULTS.encryptionKey, 'utf8'),
  supportedSaaS: process.env.SUPPORTED_SAAS
    ? process.env.SUPPORTED_SAAS.split(',')
    : DEFAULTS.supportedSaaS,
};