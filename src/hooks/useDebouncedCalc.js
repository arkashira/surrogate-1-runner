/**
 * useDebouncedCalc
 *
 * A reusable hook that debounces input changes, calls an async calculation
 * function, and exposes loading / result / error state together with a
 * convenient `debouncedCalculate` trigger.
 *
 * @param {any}          initialInput   – Initial raw input value (can be undefined).
 * @param {function}     apiFn          – Async function that receives the debounced
 *                                        input and returns the calculation result.
 *                                        Signature: async (input) => result
 * @param {number}       delay          – Debounce delay in ms (default 300).
 *
 * @returns {{
 *   result: any,
 *   loading: boolean,
 *   error: any,
 *   setInput: (newInput:any)=>void,
 *   debouncedCalculate: (input:any)=>void
 * }}
 */
import { useState, useEffect, useRef, useCallback } from "react";

export default function useDebouncedCalc(initialInput, apiFn, delay = 300) {
  // -------------------------------------------------------------------------
  // 1️⃣ State & refs
  // -------------------------------------------------------------------------
  const [rawInput, setRawInput] = useState(initialInput);
  const [debouncedInput, setDebouncedInput] = useState(initialInput);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const debounceTimer = useRef(null);
  const isMounted = useRef(true); // prevents state updates after unmount

  // -------------------------------------------------------------------------
  // 2️⃣ Mount / unmount handling
  // -------------------------------------------------------------------------
  useEffect(() => {
    return () => {
      isMounted.current = false;
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, []);

  // -------------------------------------------------------------------------
  // 3️⃣ Debounce raw → debounced value
  // -------------------------------------------------------------------------
  useEffect(() => {
    // Reset timer on every raw input change
    if (debounceTimer.current) clearTimeout(debounceTimer.current);

    debounceTimer.current = setTimeout(() => {
      setDebouncedInput(rawInput);
    }, delay);

    // Cleanup if rawInput changes before timer fires
    return () => clearTimeout(debounceTimer.current);
  }, [rawInput, delay]);

  // -------------------------------------------------------------------------
  // 4️⃣ Perform the async calculation when debounced input settles
  // -------------------------------------------------------------------------
  useEffect(() => {
    // Guard against the very first render when input may be undefined
    if (debouncedInput === undefined) return;

    let cancelled = false; // local cancellation flag for this effect run

    const runCalc = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiFn(debouncedInput);
        if (!cancelled && isMounted.current) setResult(res);
      } catch (err) {
        if (!cancelled && isMounted.current) setError(err);
      } finally {
        if (!cancelled && isMounted.current) setLoading(false);
      }
    };

    runCalc();

    // Cleanup for rapid successive changes
    return () => {
      cancelled = true;
    };
  }, [debouncedInput, apiFn]);

  // -------------------------------------------------------------------------
  // 5️⃣ Public helpers
  // -------------------------------------------------------------------------
  /** Set a new raw input – debouncing is handled automatically */
  const setInput = useCallback(
    (newInput) => {
      setRawInput(newInput);
    },
    []
  );

  /**
   * Imperative trigger that bypasses the internal raw → debounced flow.
   * Useful when you want to fire a calculation immediately (e.g. on a button click)
   * while still respecting the shared debounce timer.
   */
  const debouncedCalculate = useCallback(
    (input) => {
      // Clear any pending timer so the new call wins
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
      // Directly set the debounced value – the effect in #4 will run instantly
      setDebouncedInput(input);
    },
    []
  );

  // -------------------------------------------------------------------------
  // 6️⃣ Return API
  // -------------------------------------------------------------------------
  return {
    result,
    loading,
    error,
    setInput,
    debouncedCalculate,
  };
}