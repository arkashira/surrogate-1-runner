import axios from 'axios';

interface CostMetric {
  timestamp: string;
  cost: number;
}

export const fetchCostMetrics = async (serviceType: string, timeRange: string): Promise<CostMetric[]> => {
  try {
    const response = await axios.get('/api/cost-metrics', {
      params: {
        serviceType,
        timeRange,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching cost metrics:', error);
    throw error;
  }
};