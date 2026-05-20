/**
 * IRS API client
 *
 * This module provides a simple interface for fetching the latest IRS rule set
 * from the public API. The client implements a short‑lived in‑memory cache
 * to reduce the number of external calls. The cache expires after 1 hour.
 *
 * Usage:
 *   const { getIRSRuleSet } = require('./irsClient');
 *   const rules = await getIRSRuleSet();
 *
 * Environment Variables:
 *   IRS_API_URL   - Base URL of the IRS public API endpoint.
 *   IRS_API_TOKEN - Optional bearer token for authenticated requests.
 */

const axios = require('axios');
const { URL } = require('url');

const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

let cache = {
  data: null,
  timestamp: 0,
};

const apiUrl = process.env.IRS_API_URL;
if (!apiUrl) {
  throw new Error('Missing required environment variable: IRS_API_URL');
}

const apiToken = process.env.IRS_API_TOKEN;

/**
 * Builds the full request URL for the IRS API.
 * @returns {string}
 */
function buildRequestUrl() {
  // The public API may expose a specific endpoint for the rule set.
  // Default to `${IRS_API_URL}/rules` if not already present.
  const url = new URL(apiUrl);
  if (!url.pathname.endsWith('/rules')) {
    url.pathname = `${url.pathname.replace(/\/+$/, '')}/rules`;
  }
  return url.toString();
}

/**
 * Performs the HTTP request to the IRS API.
 * @returns {Promise<Object>} Parsed JSON response.
 */
async function fetchFromApi() {
  const requestUrl = buildRequestUrl();

  const headers = {
    Accept: 'application/json',
  };

  if (apiToken) {
    headers.Authorization = `Bearer ${apiToken}`;
  }

  const response = await axios.get(requestUrl, { headers });

  if (response.status !== 200) {
    throw new Error(`IRS API returned status ${response.status}`);
  }

  return response.data;
}

/**
 * Returns the IRS rule set, using the cache if valid.
 * @returns {Promise<Object>} The rule set JSON.
 */
async function getIRSRuleSet() {
  const now = Date.now();

  if (cache.data && now - cache.timestamp < CACHE_TTL_MS) {
    return cache.data;
  }

  const data = await fetchFromApi();
  cache = { data, timestamp: now };
  return data;
}

module.exports = {
  getIRSRuleSet,
};