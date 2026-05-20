
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const connectStripe = async () => {
  // Simulate API call - replace with actual implementation
  await delay(800);
  // In production: await fetch('/api/stripe/connect', { method: 'POST' });
  return { connected: true, accountId: 'acct_123456' };
};

export const connectGA4 = async () => {
  await delay(800);
  // In production: await fetch('/api/ga4/connect', { method: 'POST' });
  return { connected: true, propertyId: 'GA4_789' };
};

export const uploadCSV = async (file) => {
  await delay(1200);
  // In production: const formData = new FormData(); formData.append('file', file);
  return { uploaded: true, rowCount: 150 };
};

export const verifyConnections = async (status) => {
  await delay(500);
  return { verified: true, status };
};