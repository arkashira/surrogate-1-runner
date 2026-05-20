/**
 * Dashboard UI for displaying cost forecasts and budgets.
 *
 * This module renders a simple dashboard that:
 *   - Shows the forecasted next‑month cost.
 *   - Displays the current budget.
 *   - Provides a form to update the budget.
 *
 * It relies on the forecast.js and budget.js modules.
 */

import { getHistoricalUsage, forecastCost } from './forecast.js';
import { getBudget, setBudget } from './budget.js';

const dashboardEl = document.getElementById('dashboard');
if (!dashboardEl) {
  console.warn('Dashboard element not found');
  // Exit early if the container is missing
  return;
}

async function render() {
  // Clear existing content
  dashboardEl.innerHTML = '';

  // Fetch forecast data
  const usageHistory = await getHistoricalUsage();
  const forecast = forecastCost(usageHistory);

  // Fetch current budget
  const currentBudget = getBudget();

  // Create forecast section
  const forecastSection = document.createElement('section');
  forecastSection.innerHTML = `
    <h2>Cost Forecast</h2>
    <p>Projected cost for next month: <strong>$${forecast.toFixed(2)}</strong></p>
  `;
  dashboardEl.appendChild(forecastSection);

  // Create budget section
  const budgetSection = document.createElement('section');
  budgetSection.innerHTML = `
    <h2>Budget</h2>
    <p>Current budget: <strong>$${currentBudget !== null ? currentBudget.toFixed(2) : 'Not set'}</strong></p>
    <form id="budget-form">
      <label for="budget-input">Set new budget ($):</label>
      <input type="number" id="budget-input" name="budget" min="0" step="0.01" required />
      <button type="submit">Update</button>
    </form>
  `;
  dashboardEl.appendChild(budgetSection);

  // Attach form handler
  const form = document.getElementById('budget-form');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = document.getElementById('budget-input');
    const newBudget = parseFloat(input.value);
    try {
      setBudget(newBudget);
      // Re‑render to show updated budget
      render();
    } catch (err) {
      alert(err.message);
    }
  });
}

// Initial render
render();