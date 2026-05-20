/**
 * Entry point for the web‑shell UI.
 * Handles authentication, error display, and shell rendering.
 */
import { checkAuth, redirectToSAML, showAuthError } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const isAuthenticated = await checkAuth();
    if (!isAuthenticated) {
      redirectToSAML();
      return;
    }

    // Render the shell UI
    const shell = document.getElementById('shell-container');
    shell.innerHTML = `
      <h1>Welcome to the Axentx Web Shell</h1>
      <p>You are now authenticated.</p>
    `;
    shell.style.display = 'block';
  } catch (err) {
    showAuthError(err.message || 'Authentication failed');
  }
});