const redisCache = require('./redisCache');

describe('Redis Cache', () => {
  it('should set and get a value', () => {
    const key = 'test-key';
    const value = 'test-value';
    return redisCache.set(key, value).then(() => {
      return redisCache.get(key).then((reply) => {
        expect(reply).toBe(value);
      });
    });
  });

  it('should return null for a non-existent key', () => {
    const key = 'non-existent-key';
    return redisCache.get(key).then((reply) => {
      expect(reply).toBe(null);
    });
  });

  it('should return true for a cache hit', () => {
    const key = 'test-key';
    const value = 'test-value';
    return redisCache.set(key, value).then(() => {
      return redisCache.cacheHit(key).then((reply) => {
        expect(reply).toBe(true);
      });
    });
  });

  it('should return false for a cache miss', () => {
    const key = 'non-existent-key';
    return redisCache.cacheMiss(key).then((reply) => {
      expect(reply).toBe(false);
    });
  });

  it('should return cache stats', () => {
    return redisCache.cacheStats().then((stats) => {
      expect(stats).not.toBe(null);
    });
  });
});