const { getTaskStatuses } = require('../services/apiClient');
const fetch = require('node-fetch');

jest.mock('node-fetch');

describe('apiClient', () => {
  test('getTaskStatuses returns parsed task data', async () => {
    const mockResponse = {
      status: 200,
      json: () => Promise.resolve([
        { id: 'task1', status: 'running', created_at: '2026-05-04T12:00:00Z', total_data_size: 1024 },
        { id: 'task2', status: 'completed', created_at: '2026-05-04T11:00:00Z', total_data_size: 2048 }
      ])
    };
    
    fetch.mockResolvedValueOnce(mockResponse);
    
    const result = await getTaskStatuses();
    expect(result).toHaveLength(2);
    expect(result[0].status).toBe('running');
    expect(result[1].totalDataSize).toBe(2048);
  });

  test('getTaskStatuses handles errors gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Network failure'));
    const result = await getTaskStatuses();
    expect(result).toHaveLength(0);
  });
});