/**
 * Tests for the IRS API client.
 *
 * These tests use a mock server to simulate the IRS public API.
 */

const { getIRSRuleSet } = require('../../src/services/irsClient');
const nock = require('nock');

describe('IRS API Client', () => {
  const apiBase = 'https://api.irs.gov';
  const apiPath = '/rules';

  beforeAll(() => {
    process.env.IRS_API_URL = `${apiBase}${apiPath}`;
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('fetches rule set from the API', async () => {
    const mockData = { version: '2024', rules: [] };

    nock(apiBase)
      .get(apiPath)
      .reply(200, mockData);

    const data = await getIRSRuleSet();
    expect(data).toEqual(mockData);
  });

  it('caches the result for subsequent calls', async () => {
    const mockData = { version: '2024', rules: [] };

    const scope = nock(apiBase)
      .get(apiPath)
      .reply(200, mockData);

    const firstCall = await getIRSRuleSet();
    expect(firstCall).toEqual(mockData);
    expect(scope.isDone()).toBe(true);

    // Second call should hit cache, no new HTTP request
    const secondCall = await getIRSRuleSet();
    expect(secondCall).toEqual(mockData);
  });

  it('throws an error on non-200 responses', async () => {
    nock(apiBase)
      .get(apiPath)
      .reply(500);

    await expect(getIRSRuleSet()).rejects.toThrow(/status 500/);
  });
});