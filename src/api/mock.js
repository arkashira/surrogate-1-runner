import axios from 'axios';

const mockData = [
  { channel: 'Facebook', cac: 12.34, ltv: 45.67, campaign_type: 'CPC' },
  { channel: 'Google Ads', cac: 23.45, ltv: 67.89, campaign_type: 'CPC' },
  { channel: 'Email', cac: 5.67, ltv: 30.12, campaign_type: 'Email' },
];

axios.interceptors.request.use((config) => {
  if (config.url.endsWith('/api/cac_ltv')) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: mockData,
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
        });
      }, 500);
    });
  }
  return config;
});