import axios from 'axios';
import { getInstanceData } from '../../src/services/api';

jest.mock('axios');

describe('getInstanceData', () => {
  it('fetches instance data successfully', async () => {
    const mockData = { name: 'Test Instance', totalDataSize: '100 MB' };
    axios.get.mockResolvedValue({ data: mockData });

    const result = await getInstanceData('1');
    expect(result).toEqual(mockData);
  });

  it('handles errors', async () => {
    axios.get.mockRejectedValue(new Error('Network Error'));

    await expect(getInstanceData('1')).rejects.toThrow('Network Error');
  });
});