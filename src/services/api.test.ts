import axios from 'axios';
import { fetchOnboardingCompletionData } from './api';

jest.mock('axios');

describe('fetchOnboardingCompletionData', () => {
  it('fetches data successfully from the API', async () => {
    const mockData = [
      { step: 'Step 1', completionRate: 80 },
      { step: 'Step 2', completionRate: 65 },
    ];
    axios.get.mockResolvedValue({ data: mockData });

    const result = await fetchOnboardingCompletionData('week');
    expect(result).toEqual(mockData);
    expect(axios.get).toHaveBeenCalledWith('https://api.axentx.com/onboarding/completion-rates', {
      params: { timePeriod: 'week' }
    });
  });

  it('handles errors when fetching data', async () => {
    axios.get.mockRejectedValue(new Error('Network Error'));

    const result = await fetchOnboardingCompletionData('week');
    expect(result).toEqual([]);
    expect(axios.get).toHaveBeenCalledWith('https://api.axentx.com/onboarding/completion-rates', {
      params: { timePeriod: 'week' }
    });
  });
});