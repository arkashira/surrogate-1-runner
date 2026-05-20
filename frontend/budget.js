/**
 * Budget management module.
 *
 * Budgets are stored in localStorage for simplicity. In a real
 * deployment, these would be persisted via an API.
 *
 * Exports:
 *   - getBudget: retrieves the current budget value.
 *   - setBudget: updates the budget value.
 */

const STORAGE_KEY = 'axentx_budget';

export function getBudget() {
  const val = localStorage.getItem(STORAGE_KEY);
  return val ? parseFloat(val) : null;
}

export function setBudget(amount) {
  if (typeof amount !== 'number' || amount < 0) {
    throw new Error('Budget must be a non‑negative number');
  }
  localStorage.setItem(STORAGE_KEY, amount.toString());
}