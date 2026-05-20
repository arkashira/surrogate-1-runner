import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import type { CompetitiveInsightsData } from '../types/competitive-insights';

interface UseCompetitiveDataOptions {
  productId?: string;
  categoryId?: string;
  refreshInterval?: number;
  enabled?: boolean;
}

interface UseCompetitiveDataResult {
  data: CompetitiveInsightsData | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export const useCompetitiveData = ({
  productId,
  categoryId,
  refreshInterval,
  enabled = true,
}: UseCompetitiveDataOptions): UseCompetitiveDataResult => {
  const [data, setData] = useState<CompetitiveInsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    if (!enabled) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (productId) params.append('productId', productId);
      if (categoryId) params.append('categoryId', categoryId);
      
      const response = await api.get<CompetitiveInsightsData>(
        `/competitive-insights?${params.toString()}`
      );
      setData(response.data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch competitive data'));
    } finally {
      setLoading(false);
    }
  }, [enabled, productId, categoryId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    if (!refreshInterval || refreshInterval <= 0) return;
    
    const intervalId = setInterval(fetchData, refreshInterval);
    return () => clearInterval(intervalId);
  }, [refreshInterval, fetchData]);

  return { data, loading, error, refetch: fetchData };
};