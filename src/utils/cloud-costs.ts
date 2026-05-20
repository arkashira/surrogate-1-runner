import axios from 'axios';

async function getCloudCosts(): Promise<number[]> {
  const response = await axios.get('https://example.com/cloud-costs');
  return response.data;
}

export { getCloudCosts };