import api from './api';

export const analyzeFeedback = async (feedback: string) => {
  try {
    const { data } = await api.post('/feedback/analysis', { feedback });
    return data; // e.g. sentiment score, tags, etc.
  } catch (err) {
    console.error('Failed to analyze feedback', err);
    throw err;
  }
};