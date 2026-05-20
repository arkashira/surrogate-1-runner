/**
 * Authentication helper functions for the client.
 * All functions are exported so they can be unit‑tested.
 */

const AUTH_STATUS_ENDPOINT = '/api/auth/status';
const SAML_LOGIN_URL = '/saml/login';

/**
 * Checks if the current session is authenticated.
 * @returns {Promise<boolean>}
 */
export async function checkAuth() {
  const res = await fetch(AUTH_STATUS_ENDPOINT, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch auth status');
  const { authenticated } = await res.json();
  return authenticated === true;
}

/**
 * Redirects to the SAML IdP, preserving the current URL for return.
 */
export function redirectToSAML() {
  const returnTo = encodeURIComponent(window.location.pathname + window.location.search);
  window.location.href = `${SAML_LOGIN_URL}?return_to=${returnTo}`;
}

/**
 * Shows an error message in the dedicated container.
 * @param {string} msg
 */
export function showAuthError(msg) {
  const container = document.getElementById('error-container');
  container.textContent = msg;
  container.style.display = 'block';
}