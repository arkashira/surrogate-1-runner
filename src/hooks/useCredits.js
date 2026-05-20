import { useState } from 'react';
import useIntervalRefresh from './useIntervalRefresh';
import { getCredits } from '../api/credits';

/**
 * Returns the latest credit payload and a loading flag.
 * The data is refreshed automatically every `intervalMs` (default 60 s).
 *
 * @param {number} [intervalMs] – optional custom refresh interval.
 * @returns {{credits: object|null, loading: boolean}}
 */
export default function useCredits(intervalMs) {
  const [credits, setCredits] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = async () => {
    setLoading(true);
    const data = await getCredits();
    if (data) setCredits(data);
    setLoading(false);
  };

  // Leverage the generic interval hook.
  useIntervalRefresh(refresh, intervalMs);

  return { credits, loading };
}