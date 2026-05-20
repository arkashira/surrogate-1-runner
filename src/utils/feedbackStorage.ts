import api from './api';

export const storeFeedback = async (feedback: string) => {
  try {
    const { data } = await api.post('/feedback', { feedback });
    return data; // whatever the backend returns
  } catch (err) {
    console.error('Failed to store feedback', err);
    throw err;
  }
};