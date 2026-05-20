/**
 * Performance optimization utilities for MapView.
 *
 * This module provides a robust set of helpers to keep the MapView responsive
 * during heavy user interactions (panning, zooming) and data fetching.
 *
 * Strategies employed:
 * - Batching: Uses requestAnimationFrame to coalesce visual updates.
 * - Throttling: Limits the rate of function execution (time-based for network,
 *   frame-based for rendering).
 * - Debouncing: Ensures expensive operations (like state updates) only run
 *   after the user stops interacting.
 * - Memoization: Caches expensive geometric calculations.
 */

const DEFAULT_THROTTLE_MS = 100;
const DEFAULT_DEBOUNCE_MS = 200;
const FRAME_TIME_MS = 16.666;

/**
 * Batches a callback to run on the next animation frame.
 * Includes a fallback for environments without RAF and robust error handling
 * to prevent the MapView from crashing.
 *
 * @param {Function} cb - The callback to execute.
 * @returns {number} The requestAnimationFrame ID (for cancellation).
 */
export function batchOnNextFrame(cb) {
  if (typeof requestAnimationFrame === 'function') {
    return requestAnimationFrame(() => {
      try {
        cb();
      } catch (e) {
        console.error('[MapView] batchOnNextFrame error:', e);
      }
    });
  } else {
    // Fallback for SSR or older browsers
    return setTimeout(() => {
      try {
        cb();
      } catch (e) {
        console.error('[MapView] batchOnNextFrame error:', e);
      }
    }, FRAME_TIME_MS);
  }
}

/**
 * Throttles a function to run at most once per specified time interval.
 * Best for limiting API calls or heavy computations that don't need to run
 * on every single pixel of movement.
 *
 * @param {Function} fn - The function to throttle.
 * @param {number} [limit=DEFAULT_THROTTLE_MS] - Minimum time between calls in ms.
 * @returns {Function} A throttled function.
 */
export function throttle(fn, limit = DEFAULT_THROTTLE_MS) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}

/**
 * Throttles a function to run at most once per animation frame.
 * Best for visual updates (e.g., syncing a custom overlay position) to ensure
 * smooth 60fps rendering without blocking the main thread.
 *
 * @param {Function} fn - The function to throttle.
 * @returns {Function} A frame-throttled function.
 */
export function throttleFrame(fn) {
  let scheduled = false;
  return function (...args) {
    if (scheduled) return;
    scheduled = true;
    batchOnNextFrame(() => {
      scheduled = false;
      fn.apply(this, args);
    });
  };
}

/**
 * Debounces a function call, ensuring it only executes after the
 * specified delay has elapsed without a new invocation.
 * Best for updating UI state (e.g., search results) after user stops typing/panning.
 *
 * @param {Function} fn - The function to debounce.
 * @param {number} [delay=DEFAULT_DEBOUNCE_MS] - Delay in milliseconds.
 * @returns {Function} A debounced function.
 */
export function debounce(fn, delay = DEFAULT_DEBOUNCE_MS) {
  let timeoutId = null;
  return function (...args) {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      timeoutId = null;
      fn.apply(this, args);
    }, delay);
  };
}

/**
 * Memoizes a pure function based on its arguments.
 * Useful for caching expensive calculations like visible region bounds or
 * marker clustering logic.
 *
 * @param {Function} fn - Pure function to memoize.
 * @returns {Function} Memoized function.
 */
export function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// --- Contextual Helpers for MapView ---

/**
 * Creates a throttled handler for map movement events.
 * Use this for expensive operations (e.g., fetching tiles/data) that should
 * not happen on every single frame, but frequently enough to feel responsive.
 *
 * @param {Object} map - Map instance (e.g., from react-native-maps).
 * @param {Function} onMove - Callback to execute on move.
 * @returns {Function} Event handler.
 */
export function createThrottledMoveHandler(map, onMove) {
  return throttle(() => {
    const region = map.getCamera ? map.getCamera() : map.getRegion();
    onMove(region);
  }, DEFAULT_THROTTLE_MS);
}

/**
 * Creates a debounced handler for region changes.
 * Use this for state updates that trigger a re-render (e.g., updating URL params
 * or saving location) to ensure we only save the final position.
 *
 * @param {Function} onRegionChange - Callback to execute after user stops interacting.
 * @returns {Function} Event handler.
 */
export function createDebouncedRegionChangeHandler(onRegionChange) {
  return debounce((region) => {
    onRegionChange(region);
  }, DEFAULT_DEBOUNCE_MS);
}