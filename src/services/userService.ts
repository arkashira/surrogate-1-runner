import axios from 'axios';

const API_URL = 'https://api.example.com';

export const setLearningGoal = async (goal: string) => {
  try {
    await axios.post(`${API_URL}/user/learning-goal`, { goal });
  } catch (error) {
    console.error('Error setting learning goal:', error);
  }
};

export const setOnboardingFeedback = async (feedback: string) => {
  try {
    await axios.post(`${API_URL}/user/onboarding-feedback`, { feedback });
  } catch (error) {
    console.error('Error setting onboarding feedback:', error);
  }
};