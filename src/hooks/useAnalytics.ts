import { useState, useEffect, useCallback } from 'react';
import { AnalyticsRecord } from '../types/analytics';

export function useAnalytics(pollIntervalMs = 60_000) {
  const [data, setData] = useState<AnalyticsRecord[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const resp = await fetch('/api/analytics');
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const json: AnalyticsRecord[] = await resp.json();
      setData(json);
      setError(null);
    } catch (e: any) {
      setError(e.message ?? 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(); // initial load
    const timer = setInterval(fetchData, pollIntervalMs);
    return () => clearInterval(timer);
  }, [fetchData, pollIntervalMs]);

  return { data, loading, error, refetch: fetchData };
}