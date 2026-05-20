const CloudProviderFilter = require('../CloudProviderFilter');

describe('CloudProviderFilter', () => {
  const mockData = [
    { id: 1, provider: 'AWS', latency: 100, memory: 256 },
    { id: 2, provider: 'GCP', latency: 120, memory: 256 },
    { id: 3, provider: 'Azure', latency: 110, memory: 256 },
  ];

  let filter;

  beforeEach(() => {
    filter = new CloudProviderFilter(mockData);
  });

  test('should filter data by provider', () => {
    const awsData = filter.applyFilter('AWS');
    expect(awsData).toEqual([mockData[0]]);
  });

  test('should throw error for invalid provider', () => {
    expect(() => filter.applyFilter('InvalidProvider')).toThrow('Invalid cloud provider');
  });

  test('should return list of providers', () => {
    expect(filter.getProviders()).toEqual(['AWS', 'GCP', 'Azure']);
  });
});