import axios from 'axios';

/**
 * GET /api/credits
 * @returns {Promise<{monthly:{total:number,used:number,remaining:number},
 *                    bulk:{total:number,used:number,remaining:number}}|null>}
 */
export const getCredits = async () => {
  try {
    const { data } = await axios.get('/api/credits');
    return data;
  } catch (err) {
    console.error('❗️ getCredits – network error:', err);
    return null;               // callers can decide how to handle a null result
  }
};