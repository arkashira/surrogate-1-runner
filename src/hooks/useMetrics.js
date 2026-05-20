import { useState, useCallback, useEffect } from 'react';

/**
 * Hook that fetches metric data based on the supplied filters.
 *
 * @param {Object} initialFilters
 * @param {string} initialFilters.cohort   – e.g. "All"
 * @param {string} initialFilters.dateRange – e.g. "7d"
 * @param {number} refreshIntervalMs       – auto‑refresh interval (0 = disabled)
 *
 * @returns {{
 *   metrics: Object,
 *   loading: boolean,
 *   error: Error|null,
 *   filters: Object,
 *   setFilters: Function,
 *   refresh: Function
 * }}
 */
export function useMetrics(
  { cohort = 'All', dateRange = '7d' } = {},
  refreshIntervalMs = 5 * 60 * 1000 // 5 min default
) {
  const [filters, setFilters] = useState({ cohort, dateRange });
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams(filters);
      const res = await fetch(`/api/metrics?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setMetrics(data);
    } catch (e) {
      console.error('Failed to fetch metrics', e);
      setError(e);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Initial load + optional auto‑refresh
  useEffect(() => {
    fetchMetrics();
    if (refreshIntervalMs > 0) {
      const id = setInterval(fetchMetrics, refreshIntervalMs);
      return () => clearInterval(id);
    }
  }, [fetchMetrics, refreshIntervalMs]);

  return {
    metrics,
    loading,
    error,
    filters,
    setFilters,
    refresh: fetchMetrics,
  };
}