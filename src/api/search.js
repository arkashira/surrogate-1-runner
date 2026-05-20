const axios = require('axios');

const SEARCH_API_URL = 'https://api.axentx.com/search';

class SearchAPI {
  static async search(query) {
    try {
      const response = await axios.get(`${SEARCH_API_URL}?q=${encodeURIComponent(query)}`);
      return response.data.results;
    } catch (error) {
      console.error('Search API error:', error);
      throw error;
    }
  }
}

module.exports = SearchAPI;