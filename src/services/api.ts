import axios from 'axios';
import { ResourceBreakdown, TimeRange } from '../types';

const API_BASE_URL = 'https://api.axentx.com';

export const fetchRootCauseData = async (alertId: string, timeRange: TimeRange): Promise<ResourceBreakdown[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/alerts/${alertId}/root-cause`, {
      params: { timeRange },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch root cause data:', error);
    throw error;
  }
};