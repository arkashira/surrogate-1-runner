const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

class GrammarCorrectionAPI {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.grammarcorrection.com/v1';
    this.userHistory = {};
  }

  async correctGrammar(text) {
    const requestId = uuidv4();
    const endpoint = `${this.baseUrl}/correct?text=${encodeURIComponent(text)}`;

    try {
      const response = await axios.get(endpoint, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'X-Request-ID': requestId
        }
      });

      const correctedText = response.data.corrected_text;
      this._trackImprovement(text, correctedText, requestId);
      return correctedText;
    } catch (error) {
      console.error('Error correcting grammar:', error);
      throw error;
    }
  }

  _trackImprovement(originalText, correctedText, requestId) {
    const userId = 'current_user_id'; // Replace with actual user ID logic
    if (!this.userHistory[userId]) {
      this.userHistory[userId] = [];
    }

    this.userHistory[userId].push({
      requestId,
      originalText,
      correctedText,
      timestamp: new Date().toISOString()
    });
  }

  getUserHistory(userId) {
    return this.userHistory[userId] || [];
  }
}

module.exports = GrammarCorrectionAPI;