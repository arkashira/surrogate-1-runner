import axios from 'axios';

export const getFeedbacks = async () => {
  try {
    const response = await axios.get('/api/feedbacks');
    return response.data;
  } catch (error) {
    console.error("Error fetching feedbacks:", error);
    throw error; // Re-throw to allow component-level handling
  }
};