import { fetchComponentBenchmarks } from '../api';

jest.mock('node-fetch');

describe('fetchComponentBenchmarks', () => {
  it('should fetch and return benchmark data', async () => {
    const mockData = [
      { test_name: 'Latency', value: '12ms', unit: 'ms' },
      { test_name: 'Throughput', value: '4500', unit: 'TPS' }
    ];
    
    global.fetch = jest.fn(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockData)
      })
    );
    
    const result = await fetchComponentBenchmarks('cpu-789');
    expect(result).toEqual(mockData);
  });

  it('should handle API errors', async () => {
    global.fetch = jest.fn(() => 
      Promise.resolve({
        ok: false,
        status: 500
      })
    );
    
    await expect(fetchComponentBenchmarks('gpu-456'))
      .rejects
      .toThrow('Benchmark data fetch failed');
  });
});