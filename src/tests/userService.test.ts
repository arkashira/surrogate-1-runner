import axios from 'axios';
import { setLearningGoal, setOnboardingFeedback } from '../services/userService';

jest.mock('axios');

describe('userService', () => {
  it('sets learning goal', async () => {
    const mockPost = axios.post as jest.MockedFunction<typeof axios.post>;
    mockPost.mockResolvedValueOnce({ data: {} });

    await setLearningGoal('Learn React');
    expect(mockPost).toHaveBeenCalledWith('https://api.example.com/user/learning-goal', { goal: 'Learn React' });
  });

  it('sets onboarding feedback', async () => {
    const mockPost = axios.post as jest.MockedFunction<typeof axios.post>;
    mockPost.mockResolvedValueOnce({ data: {} });

    await setOnboardingFeedback('Great onboarding experience');
    expect(mockPost).toHaveBeenCalledWith('https://api.example.com/user/onboarding-feedback', { feedback: 'Great onboarding experience' });
  });
});