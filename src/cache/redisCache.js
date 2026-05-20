const redis = require('redis');
const client = redis.createClient({
  host: 'localhost',
  port: 6379,
});

const cache = {};

client.on('connect', () => {
  console.log('Connected to Redis');
});

client.on('error', (err) => {
  console.log(`Error: ${err}`);
});

const get = (key, ttl = 60) => {
  return new Promise((resolve, reject) => {
    client.get(key, (err, reply) => {
      if (err) {
        reject(err);
      } else {
        if (reply) {
          resolve(reply);
        } else {
          resolve(null);
        }
      }
    });
  });
};

const set = (key, value, ttl = 60) => {
  return new Promise((resolve, reject) => {
    client.setex(key, ttl, value, (err, reply) => {
      if (err) {
        reject(err);
      } else {
        resolve(reply);
      }
    });
  });
};

const cacheHit = (key) => {
  return get(key).then((reply) => {
    if (reply) {
      return true;
    } else {
      return false;
    }
  });
};

const cacheMiss = (key) => {
  return get(key).then((reply) => {
    if (!reply) {
      return true;
    } else {
      return false;
    }
  });
};

const cacheStats = () => {
  return new Promise((resolve, reject) => {
    client.hgetall('cache:stats', (err, reply) => {
      if (err) {
        reject(err);
      } else {
        resolve(reply);
      }
    });
  });
};

module.exports = {
  get,
  set,
  cacheHit,
  cacheMiss,
  cacheStats,
};