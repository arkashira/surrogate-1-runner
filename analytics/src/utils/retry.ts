export async function retry<T>(
  fn: () => Promise<T>,
  attempts = 5,
  baseDelayMs = 250
): Promise<T> {
  let lastError: any;
  for (let i = 0; i < attempts; i++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e;
      const delay = baseDelayMs * 2 ** i + Math.random() * 100;
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw lastError;
}