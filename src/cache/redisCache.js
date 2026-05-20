const redis = require('redis');
const { promisify } = require('util');
const cacheMetrics = require('../monitoring/cacheMetrics');

class RedisCache {
  constructor(options = {}) {
    this.client = redis.createClient(options);
    this.getAsync = promisify(this.client.get).bind(this.client);
    this.setAsync = promisify(this.client.set).bind(this.client);
    this.delAsync = promisify(this.client.del).bind(this.client);
    this.expireAsync = promisify(this.client.expire).bind(this.client);
    
    // Default TTLs for different request types (in seconds)
    this.defaultTTLs = {
      'dataset': 3600,        // 1 hour
      'metadata': 1800,       // 30 minutes
      'processing': 900,      // 15 minutes
      'result': 7200,        // 2 hours
      'default': 600         // 10 minutes
    };
    
    // Override with provided TTLs
    if (options.ttls) {
      Object.assign(this.defaultTTLs, options.ttls);
    }
    
    // Connect to Redis
    this.client.on('connect', () => {
      console.log('Connected to Redis');
    });
    
    this.client.on('error', (err) => {
      console.error('Redis error:', err);
    });
  }
  
  /**
   * Get value from cache
   * @param {string} key - Cache key
   * @returns {Promise<any>} - Cached value or null if not found
   */
  async get(key) {
    try {
      const value = await this.getAsync(key);
      if (value) {
        cacheMetrics.recordHit(key);
        return JSON.parse(value);
      }
      cacheMetrics.recordMiss(key);
      return null;
    } catch (error) {
      cacheMetrics.recordMiss(key);
      console.error('Cache get error:', error);
      return null;
    }
  }
  
  /**
   * Set value in cache with TTL
   * @param {string} key - Cache key
   * @param {any} value - Value to cache
   * @param {string} [type='default'] - Request type for TTL selection
   * @returns {Promise<boolean>} - True if successful
   */
  async set(key, value, type = 'default') {
    try {
      const ttl = this.defaultTTLs[type] || this.defaultTTLs.default;
      const serializedValue = JSON.stringify(value);
      
      await this.setAsync(key, serializedValue);
      await this.expireAsync(key, ttl);
      
      return true;
    } catch (error) {
      console.error('Cache set error:', error);
      return false;
    }
  }
  
  /**
   * Delete value from cache
   * @param {string} key - Cache key
   * @returns {Promise<boolean>} - True if successful
   */
  async del(key) {
    try {
      await this.delAsync(key);
      return true;
    } catch (error) {
      console.error('Cache delete error:', error);
      return false;
    }
  }
  
  /**
   * Check if key exists in cache
   * @param {string} key - Cache key
   * @returns {Promise<boolean>} - True if key exists
   */
  async exists(key) {
    try {
      const result = await promisify(this.client.exists).bind(this.client)(key);
      return result === 1;
    } catch (error) {
      console.error('Cache exists error:', error);
      return false;
    }
  }
  
  /**
   * Get TTL for a key
   * @param {string} key - Cache key
   * @returns {Promise<number>} - TTL in seconds
   */
  async ttl(key) {
    try {
      return await promisify(this.client.ttl).bind(this.client)(key);
    } catch (error) {
      console.error('Cache TTL error:', error);
      return -1;
    }
  }
  
  /**
   * Close Redis connection
   */
  quit() {
    return this.client.quit();
  }
}

module.exports = RedisCache;