import axios from 'axios';

export const fetchRecommendations = async (budget: number, targetGame: string) => {
  try {
    const response = await axios.get('/api/upgrade-recommendations', {
      params: {
        budget,
        targetGame,
      },
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch upgrade recommendations');
  }
};