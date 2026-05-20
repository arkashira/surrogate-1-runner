const api = require('./api');
const axios = require('axios');

jest.mock('axios');

describe('API Service', () => {
  describe('getRecordings', () => {
    it('should fetch recordings successfully', async () => {
      const mockRecordings = [
        { id: 1, title: 'Recording 1', duration: '00:10:00', status: 'completed' },
        { id: 2, title: 'Recording 2', duration: '00:20:00', status: 'completed' },
      ];
      axios.get.mockResolvedValue({ data: mockRecordings });

      const recordings = await api.getRecordings();
      expect(recordings).toEqual(mockRecordings);
      expect(axios.get).toHaveBeenCalledWith('http://localhost:3001/api/recordings');
    });

    it('should handle errors when fetching recordings', async () => {
      const errorMessage = 'Network Error';
      axios.get.mockRejectedValue(new Error(errorMessage));

      await expect(api.getRecordings()).rejects.toThrow(errorMessage);
    });
  });
});