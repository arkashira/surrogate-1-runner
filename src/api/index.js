import axios from 'axios';

/**
 * Axios instance with base URL and timeout.
 * In production, replace `baseURL` with your backend endpoint.
 */
const api = axios.create({
  baseURL: '/api',
  timeout: 10_000,
});

/**
 * Fetch CAC/LTV data with optional filters.
 *
 * @param {Object} [options]
 * @param {Date}   [options.start]   Start date for the range
 * @param {Date}   [options.end]     End date for the range
 * @param {string} [options.campaign_type]  Campaign type filter
 * @returns {Promise<Array>}  Array of rows
 */
export const fetchCacLtv = async ({
  start,
  end,
  campaign_type,
} = {}) => {
  const params = {};
  if (start) params.start = start.toISOString();
  if (end) params.end = end.toISOString();
  if (campaign_type) params.campaign_type = campaign_type;

  const { data } = await api.get('/cac_ltv', { params });
  return data;
};

export default api;