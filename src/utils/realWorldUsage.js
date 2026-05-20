const API_URL = 'https://api.example.com/usage-data';

export const fetchRealWorldUsageData = async (componentId) => {
  const response = await fetch(`${API_URL}?componentId=${componentId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch usage data');
  }
  const data = await response.json();
  return data;
};