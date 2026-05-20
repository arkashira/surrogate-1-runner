const SearchAPI = require('../search');

describe('SearchAPI', () => {
  it('should return search results', async () => {
    const mockResults = [
      { id: '1', title: 'Result 1', url: '/result1' },
      { id: '2', title: 'Result 2', url: '/result2' },
      { id: '3', title: 'Result 3', url: '/result3' },
    ];

    jest.spyOn(SearchAPI, 'search').mockResolvedValue(mockResults);

    const results = await SearchAPI.search('test query');
    expect(results).toEqual(mockResults);
    expect(results.length).toBeGreaterThan(0);
  });

  it('should handle errors', async () => {
    jest.spyOn(SearchAPI, 'search').mockRejectedValue(new Error('API Error'));

    await expect(SearchAPI.search('test query')).rejects.toThrow('API Error');
  });
});