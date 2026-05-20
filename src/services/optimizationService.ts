import axios from 'axios';
import { Instance, AlternativeInstance, UtilizationMap } from '../types';

const API_BASE = '/api';

export const getInstanceUtilization = async (): Promise<UtilizationMap> => {
  const response = await axios.get<UtilizationMap>(`${API_BASE}/instance-utilization`);
  return response.data;
};

export const getAlternativeInstances = async (instanceId: string): Promise<AlternativeInstance[]> => {
  const response = await axios.get<AlternativeInstance[]>(`${API_BASE}/alternative-instances/${instanceId}`);
  return response.data;
};

export const applyOptimization = async (instanceId: string, alternativeId: string): Promise<void> => {
  await axios.post(`${API_BASE}/optimize-instance`, {
    instanceId,
    alternativeId
  });
};