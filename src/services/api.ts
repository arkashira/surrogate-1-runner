import axios from 'axios';

const API_BASE_URL = 'https://api.example.com';

export const getCostMetrics = async () => {
  const response = await axios.get(`${API_BASE_URL}/cost-metrics`);
  return response.data;
};

export const getPolicyDecisions = async () => {
  const response = await axios.get(`${API_BASE_URL}/policy-decisions`);
  return response.data;
};