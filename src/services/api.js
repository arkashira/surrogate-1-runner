import fetch from 'node-fetch';

/**
 * Generic HTTP client wrapper for the Stripe API.
 *
 * @param {string} endpoint - Full URL to request.
 * @param {object} options  - Fetch options.
 * @returns {Promise<object>}  Parsed JSON response.
 */
export async function request(endpoint, options = {}) {
  const response = await fetch(endpoint, options);

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `API request failed: ${response.status} ${response.statusText} - ${errorBody}`
    );
  }

  return response.json();
}

/**
 * GET helper.
 */
export async function get(url, headers = {}) {
  return request(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  });
}

/**
 * POST helper.
 */
export async function post(url, body = {}, headers = {}) {
  return request(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: JSON.stringify(body),
  });
}