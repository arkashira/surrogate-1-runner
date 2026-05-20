/**
 * Simple guided‑setup script that polls the SetupService for progress
 * and logs each step to the console.  In a real UI this would update
 * the DOM to show step numbers and completion feedback.
 */

const API_BASE = '/api/setup';

async function fetchStatus() {
  const res = await fetch(`${API_BASE}/status`);
  return res.json();
}

async function advanceStep() {
  const res = await fetch(`${API_BASE}/next`, { method: 'POST' });
  return res.json();
}

async function runSetup() {
  console.log('Starting guided setup...');
  let status = await fetchStatus();

  while (!status.complete) {
    console.log(`Step ${status.step + 1}: ${status.message}`);
    status = await advanceStep();
  }

  console.log('Setup complete! 🎉');
}

// Expose the run function so it can be called from the page.
window.runSetup = runSetup;

// Automatically start the setup when the page loads.
document.addEventListener('DOMContentLoaded', () => {
  runSetup().catch(err => console.error('Setup failed:', err));
});