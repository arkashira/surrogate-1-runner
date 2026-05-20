const ApiClient = require('./api');
const config = require('../config');

class HubSpotService {
  constructor() {
    if (!config.hubspotApiKey) throw new Error('HUBSPOT_API_KEY is missing');
    this.client = new ApiClient(config.hubspotBaseUrl, config.hubspotApiKey);
  }

  // Get a list of marketing contacts
  async getMarketingContacts() {
    const data = await this.client.get('/crm/v3/objects/contacts', {
      limit: 100,
      properties: ['email', 'firstname', 'lastname', 'createdate'],
    });
    return data.results || [];
  }

  // Get specific contact by ID
  async getContactById(contactId) {
    return await this.client.get(`/crm/v3/objects/contacts/${contactId}`);
  }

  // Get events for a marketing email
  async getEmailEvents(emailId) {
    const data = await this.client.get(`/marketing/v3/marketing-emails/${emailId}/events`);
    return data.results || [];
  }

  // Create a new marketing email campaign
  async createMarketingEmail(payload) {
    return await this.client.post('/marketing/v3/marketing-emails', payload);
  }
}

module.exports = new HubSpotService();