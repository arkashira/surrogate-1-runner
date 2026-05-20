const API_BASE = '/api';

/**
 * Fetch daily costs for the current month
 * @returns {Promise<Array<{date: string, cost: number}>>}
 */
export async function fetchDailyCosts() {
  const response = await fetch(`${API_BASE}/costs/daily`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch daily costs: ${response.status} ${errorText}`);
  }

  const data = await response.json();

  // Basic validation
  if (!Array.isArray(data)) {
    throw new Error('Invalid data format: expected an array');
  }

  return data.map(item => ({
    date: item.date,
    cost: Number(item.cost),
  }));
}

/**
 * Fetch budget status
 * @returns {Promise<{used: number, total: number, threshold: number}>}
 */
export async function fetchBudgetStatus() {
  const response = await fetch(`${API_BASE}/costs/budget`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch budget status: ${response.status} ${errorText}`);
  }

  return response.json();
}