/**
 * Generic HTTP API helper used by service connectors.
 *
 * Abstracts request construction, error handling, and authentication headers.
 * Requires only `node-fetch` (existing project dependency).
 *
 * Usage:
 *   const { request } = require('./api');
 *   const data = await request({
 *     method: 'GET',
 *     url: 'https://api.example.com/v1/resource',
 *     headers: { Authorization: `Bearer ${token}` }
 *   });
 *
 * @module api
 */

const fetch = require('node-fetch');

/**
 * @typedef {Object} ApiRequestOptions
 * @property {string} [method='GET'] - HTTP method (GET, POST, PUT, DELETE, etc.)
 * @property {string} url - Full endpoint URL
 * @property {Object<string,string>} [headers] - Optional request headers
 * @property {any} [body] - Optional request body (JSON-stringified if provided)
 */

/**
 * Perform an HTTP request and return the parsed response.
 *
 * @param {ApiRequestOptions} options - Request configuration
 * @returns {Promise<any>} Parsed JSON response, or raw text if not JSON
 * @throws {Error} on non-2xx responses or network failures
 */
async function request({ method = 'GET', url, headers = {}, body = null } = {}) {
  const fetchOptions = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  };

  if (body !== null && body !== undefined) {
    fetchOptions.body = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(url, fetchOptions);
  } catch (err) {
    throw new Error(`Network error while calling ${url}: ${err.message}`);
  }

  // Handle non-2xx responses with detailed error information
  if (!response.ok) {
    const responseText = await response.text();
    let parsed;
    try {
      parsed = JSON.parse(responseText);
    } catch {
      parsed = responseText;
    }

    const error = new Error(
      `API request failed (${response.status} ${response.statusText}): ${JSON.stringify(parsed, null, 2)}`
    );
    error.status = response.status;
    error.response = parsed;
    throw error;
  }

  // Parse response based on content-type (best of both approaches)
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return await response.json();
  }

  return await response.text();
}

module.exports = { request };