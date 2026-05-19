class RateLimitStore {
  constructor(quota = 5, windowMs = 60000) {
    this.quota = quota;
    this.windowMs = windowMs;
    this.store = new Map();
  }

  check(apiKey) {
    const now = Date.now();
    const record = this.store.get(apiKey);

    if (!record) {
      this.store.set(apiKey, {
        count: 1,
        windowStart: now,
      });
      return { allowed: true };
    }

    const { count, windowStart } = record;

    if (now - windowStart >= this.windowMs) {
      this.store.set(apiKey, {
        count: 1,
        windowStart: now,
      });
      return { allowed: true };
    }

    if (count >= this.quota) {
      const retryAfter = Math.ceil((this.windowMs - (now - windowStart)) / 1000);
      return { allowed: false, retryAfter };
    }

    this.store.set(apiKey, {
      count: count + 1,
      windowStart,
    });
    return { allowed: true };
  }

  reset() {
    this.store.clear();
  }
}

module.exports = RateLimitStore;