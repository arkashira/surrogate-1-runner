const nock = require('nock');
const hubspotService = require('../src/services/hubspot');
const config = require('../src/config');

describe('HubSpotService', () => {
  const baseUrl = 'https://api.hubapi.com';
  
  // Mock config for tests
  beforeAll(() => { config.hubspotApiKey = 'test-key'; });
  afterEach(() => { nock.cleanAll(); });

  test('getMarketingContacts returns array', async () => {
    const mockData = { results: [{ id: '1', properties: { email: 'test@test.com' } }] };
    nock(baseUrl).get('/crm/v3/objects/contacts').query(true).reply(200, mockData);

    const contacts = await hubspotService.getMarketingContacts();
    expect(contacts).toHaveLength(1);
    expect(contacts[0].properties.email).toBe('test@test.com');
  });

  test('createMarketingEmail creates campaign', async () => {
    const payload = { name: 'Summer Sale' };
    const mockResponse = { id: 'camp_123', ...payload };
    
    nock(baseUrl)
      .post('/marketing/v3/marketing-emails', payload)
      .reply(201, mockResponse);

    const result = await hubspotService.createMarketingEmail(payload);
    expect(result.id).toBe('camp_123');
  });
});