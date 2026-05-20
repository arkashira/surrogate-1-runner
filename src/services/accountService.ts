import axios from 'axios';

const API_BASE = '/api/retirement';

export type Provider = '401k' | 'IRA' | 'RothIRA' | '401kPlus';

/**
 * Simulate an OAuth flow.
 * Replace this with a real redirect in production.
 */
export async function authenticateProvider(provider: Provider): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(`mock-token-for-${provider}`), 500);
  });
}

/**
 * Validate the account credentials before we even try to link.
 */
export async function validateAccount(provider: Provider, accountId: string): Promise<boolean> {
  try {
    const { data } = await axios.post(`${API_BASE}/validate`, { provider, accountId });
    return data.valid;
  } catch (err) {
    console.error('Validation error:', err);
    throw new Error('Validation service unavailable.');
  }
}

/**
 * Persist the linked account (token + provider + id).
 */
export async function linkAccount(provider: Provider, accountId: string, token: string) {
  try {
    const { data } = await axios.post(`${API_BASE}/link`, { provider, accountId, token });
    return data; // { id, provider, accountId, name, ... }
  } catch (err) {
    console.error('Linking error:', err);
    throw new Error('Failed to link account.');
  }
}

/**
 * Pull the latest data for a linked account.
 */
export async function fetchAccountData(accountId: string) {
  try {
    const { data } = await axios.get(`${API_BASE}/accounts/${accountId}`);
    return data;
  } catch (err) {
    console.error(`Fetch error for ${accountId}:`, err);
    throw new Error(`Failed to fetch account data.`);
  }
}

/**
 * Start a daily sync for all linked accounts.
 * Returns the interval ID so callers can clear it.
 */
export function startAutoSync(
  accountIds: string[],
  onSync: (id: string, data: any) => void
): NodeJS.Timeout {
  const intervalMs = 24 * 60 * 60 * 1000; // 24h

  const sync = async () => {
    for (const id of accountIds) {
      try {
        const data = await fetchAccountData(id);
        onSync(id, data);
      } catch (e) {
        console.error(`Sync error for ${id}:`, e);
      }
    }
  };

  // Kick off immediately
  sync();

  return setInterval(sync, intervalMs);
}