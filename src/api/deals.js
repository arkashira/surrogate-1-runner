import axios from 'axios';

/**
 * Returns a promise that resolves to an array of deal objects.
 * The shape matches the DealList component expectations:
 *   { id, title, status, investorName?, updated_at }
 */
export const getDeals = () =>
  axios.get('/api/deals').then((res) => res.data);