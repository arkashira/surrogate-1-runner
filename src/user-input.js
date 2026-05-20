/**
 * user-input.js
 *
 * Validates raw payload from the front‑end and returns a *normalized* object
 * that the calculation layer can rely on.
 *
 * Accepted payload shapes:
 *   1️⃣ Simple flat shape (Candidate 1)
 *        { income, fixedExpenses, variableExpenses, savingsGoal? }
 *
 *   2️⃣ Rich expense map (Candidate 2)
 *        { income, expenses: { rent, utilities, … }, savingsGoal }
 *
 * The function normalises both into:
 * {
 *   income: number,
 *   expenses: { [category]: number },   // every key present, missing → 0
 *   savingsGoal: number                 // defaults to 0
 * }
 */

const REQUIRED_FIELDS = ['income', 'expenses']; // `expenses` may be an object or flat numbers

/**
 * Throws if the payload is malformed.
 * @param {object} raw
 */
function validateRawInput(raw) {
  if (typeof raw !== 'object' || raw === null) {
    throw new TypeError('Payload must be a non‑null object');
  }

  // income is always required
  if (!('income' in raw)) {
    throw new Error('Missing required field: income');
  }
  if (typeof raw.income !== 'number' || raw.income < 0) {
    throw new Error('Income must be a non‑negative number');
  }

  // savingsGoal is optional – default to 0 later
  if ('savingsGoal' in raw && (typeof raw.savingsGoal !== 'number' || raw.savingsGoal < 0)) {
    throw new Error('Savings goal must be a non‑negative number');
  }

  // Determine which expense representation we received
  const hasExpenseMap = typeof raw.expenses === 'object' && raw.expenses !== null;
  const hasFlatExpenses = 'fixedExpenses' in raw || 'variableExpenses' in raw;

  if (!hasExpenseMap && !hasFlatExpenses) {
    throw new Error(
      'Payload must contain either an "expenses" object or "fixedExpenses"/"variableExpenses" numbers'
    );
  }

  // Validate expense map if present
  if (hasExpenseMap) {
    for (const [cat, amt] of Object.entries(raw.expenses)) {
      if (typeof amt !== 'number' || amt < 0) {
        throw new Error(`Expense "${cat}" must be a non‑negative number`);
      }
    }
  }

  // Validate flat numbers if present
  if (hasFlatExpenses) {
    const { fixedExpenses = 0, variableExpenses = 0 } = raw;
    if (typeof fixedExpenses !== 'number' || fixedExpenses < 0) {
      throw new Error('fixedExpenses must be a non‑negative number');
    }
    if (typeof variableExpenses !== 'number' || variableExpenses < 0) {
      throw new Error('variableExpenses must be a non‑negative number');
    }
  }
}

/**
 * Normalises the payload into a canonical shape.
 * @param {object} raw
 * @returns {{ income: number, expenses: Record<string, number>, savingsGoal: number }}
 */
function normalizeInput(raw) {
  // Validation first – will throw on any problem
  validateRawInput(raw);

  const income = Number(raw.income);
  const savingsGoal = raw.savingsGoal ? Number(raw.savingsGoal) : 0;

  // Build a flat expenses map
  const expenses = {};

  // 1️⃣ If an explicit map was supplied, copy it (ensuring deterministic order)
  if (typeof raw.expenses === 'object' && raw.expenses !== null) {
    const sortedKeys = Object.keys(raw.expenses).sort(); // deterministic ordering
    for (const key of sortedKeys) {
      expenses[key] = Number(raw.expenses[key]);
    }
  }

  // 2️⃣ Merge flat numbers into the map (they become their own categories)
  if ('fixedExpenses' in raw) {
    expenses.fixed = Number(raw.fixedExpenses);
  }
  if ('variableExpenses' in raw) {
    expenses.variable = Number(raw.variableExpenses);
  }

  // Ensure at least an empty object (helps downstream code)
  return { income, expenses, savingsGoal };
}

module.exports = {
  validateRawInput,
  normalizeInput,
};