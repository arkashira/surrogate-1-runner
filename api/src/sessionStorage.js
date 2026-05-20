/**
 * A tiny session storage wrapper that works both in browsers and in Node
 * environments (e.g., during tests). It serialises values to JSON and
 * prefixes keys to avoid collisions.
 *
 * The API mirrors the standard Web Storage API but falls back to an in‑memory
 * store if `localStorage` is not available.
 */

const PREFIX = 'axentx:';

let _storage = null;

// Detect if localStorage is usable (e.g., in a browser)
function _hasLocalStorage() {
  try {
    const testKey = '__axentx_test__';
    window.localStorage.setItem(testKey, testKey);
    window.localStorage.removeItem(testKey);
    return true;
  } catch (_) {
    return false;
  }
}

if (_hasLocalStorage()) {
  _storage = window.localStorage;
} else {
  // In-memory fallback for Node / test environments
  _storage = {
    _data: {},
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(this._data, key)
        ? this._data[key]
        : null;
    },
    setItem(key, value) {
      this._data[key] = value;
    },
    removeItem(key) {
      delete this._data[key];
    },
    clear() {
      this._data = {};
    },
  };
}

/**
 * Stores a value under the given key.
 *
 * @param {string} key
 * @param {*} value
 */
export function set(key, value) {
  try {
    const stored = JSON.stringify(value);
    _storage.setItem(PREFIX + key, stored);
  } catch (e) {
    // Silently ignore errors (e.g., quota exceeded)
  }
}

/**
 * Retrieves a value for the given key.
 *
 * @param {string} key
 * @param {*} [defaultValue] - Returned if the key is missing or parsing fails.
 * @returns {*}
 */
export function get(key, defaultValue = null) {
  try {
    const raw = _storage.getItem(PREFIX + key);
    if (raw === null) return defaultValue;
    return JSON.parse(raw);
  } catch (e) {
    return defaultValue;
  }
}

/**
 * Removes the value stored under the given key.
 *
 * @param {string} key
 */
export function remove(key) {
  try {
    _storage.removeItem(PREFIX + key);
  } catch (_) {
    // ignore
  }
}

/**
 * Clears all keys stored by this module.
 */
export function clear() {
  try {
    // Only clear keys that belong to this module
    const keys = Object.keys(_storage._data || {}).filter((k) =>
      k.startsWith(PREFIX)
    );
    keys.forEach((k) => _storage.removeItem(k));
  } catch (_) {
    // ignore
  }
}

export default {
  set,
  get,
  remove,
  clear,
};