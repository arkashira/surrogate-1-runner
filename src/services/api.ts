import axios from 'axios';

const API_BASE_URL = 'https://api.axentx.com';

export const fetchOnboardingCompletionData = async (timePeriod) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/onboarding/completion-rates`, {
      params: { timePeriod }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching onboarding completion data:', error);
    return [];
  }
};