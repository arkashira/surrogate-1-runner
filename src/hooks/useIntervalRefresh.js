import { useEffect, useRef } from 'react';

/**
 * Runs `callback` every `intervalMs` milliseconds.
 * - Guarantees only one interval exists.
 * - Pauses when the document is hidden (tab inactive) to avoid wasteful traffic.
 * - Always calls the *latest* version of `callback` without recreating the timer.
 *
 * @param {Function} callback      Function to invoke on each tick.
 * @param {number}   intervalMs    Interval in ms (default 60 000 ms = 1 min).
 */
export default function useIntervalRefresh(callback, intervalMs = 60000) {
  const savedCallback = useRef(callback);
  const intervalId = useRef(null);

  // Keep the most recent callback reference.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (typeof savedCallback.current !== 'function') return;

    const tick = () => {
      if (document.hidden) return;   // skip when the page is not visible
      savedCallback.current();
    };

    // Immediate first run so UI isn’t stale on mount.
    tick();

    intervalId.current = setInterval(tick, intervalMs);

    return () => {
      clearInterval(intervalId.current);
      intervalId.current = null;
    };
  }, [intervalMs]);
}