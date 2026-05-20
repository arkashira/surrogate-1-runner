import axios from 'axios';
import { useState, useEffect } from 'react';
import { StartupBenchmark, BenchmarkFilters } from './types';

/**
 * In‑memory cache for benchmark data.
 * The hook will populate this once per page load.
 */
let cachedData: StartupBenchmark[] | null = null;

/**
 * Fetch benchmark data from the API endpoint.
 * If the cache is populated, it returns the cached copy.
 */
async function fetchBenchmarkData(): Promise<StartupBenchmark[]> {
  if (cachedData) return cachedData;

  const response = await axios.get<StartupBenchmark[]>('/api/benchmark');
  cachedData = response.data;
  return cachedData;
}

/**
 * React hook that fetches, filters, and exposes benchmark data.
 *
 * @param filters Optional filter criteria.
 * @returns { data, loading, error }
 */
export function useBenchmark(
  filters: BenchmarkFilters = {}
): { data: StartupBenchmark[]; loading: boolean; error: string | null } {
  const [data, setData] = useState<StartupBenchmark[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const all = await fetchBenchmarkData();

        // Apply filters
        let filtered = all;
        if (filters.minMarketSize !== undefined) {
          filtered = filtered.filter(b => b.marketSize >= filters.minMarketSize!);
        }
        if (filters.maxMarketSize !== undefined) {
          filtered = filtered.filter(b => b.marketSize <= filters.maxMarketSize!);
        }
        if (filters.minTeamExperience !== undefined) {
          filtered = filtered.filter(b => b.teamExperience >= filters.minTeamExperience!);
        }
        if (filters.maxTeamExperience !== undefined) {
          filtered = filtered.filter(b => b.teamExperience <= filters.maxTeamExperience!);
        }
        if (filters.stage) {
          filtered = filtered.filter(b => b.stage === filters.stage);
        }

        if (!cancelled) setData(filtered);
      } catch (e: any) {
        if (!cancelled) setError(e.message || 'Unknown error');
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    load();

    return () => { cancelled = true; };
  }, [filters]);

  return { data, loading, error };
}

/**
 * Predicate‑based filtering helper (useful outside React).
 */
export async function filterBenchmark(
  predicate: (item: StartupBenchmark) => boolean
): Promise<StartupBenchmark[]> {
  const data = await fetchBenchmarkData();
  return data.filter(predicate);
}

/**
 * Render benchmark data as a Markdown table.
 *
 * @param data Array of StartupBenchmark objects.
 * @param columns Optional list of columns to include.
 */
export function renderBenchmarkTable(
  data: StartupBenchmark[],
  columns?: (keyof StartupBenchmark)[]
): string {
  const allColumns: (keyof StartupBenchmark)[] = [
    'id',
    'name',
    'marketSize',
    'teamExperience',
    'funding',
    'stage',
  ];
  const selected = columns ?? allColumns;

  const header = selected.map(c => c.toString()).join(' | ');
  const separator = selected.map(() => '---').join(' | ');

  const rows = data.map(item => {
    return selected
      .map(c => {
        const v = item[c];
        return typeof v === 'number' ? v.toLocaleString() : v;
      })
      .join(' | ');
  });

  return [header, separator, ...rows].join('\n');
}