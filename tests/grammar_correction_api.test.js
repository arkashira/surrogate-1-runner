const GrammarCorrectionAPI = require('../grammar_correction_api');
const axios = require('axios');

jest.mock('axios');

describe('GrammarCorrectionAPI', () => {
  let api;

  beforeEach(() => {
    api = new GrammarCorrectionAPI('test-api-key');
    axios.get.mockReset();
  });

  it('should correct grammar successfully', async () => {
    const mockResponse = { data: { corrected_text: 'This is a corrected sentence.' } };
    axios.get.mockResolvedValue(mockResponse);

    const result = await api.correctGrammar('This is a sentence with grammar mistakes.');
    expect(result).toBe('This is a corrected sentence.');
    expect(axios.get).toHaveBeenCalledWith(
      'https://api.grammarcorrection.com/v1/correct?text=This%20is%20a%20sentence%20with%20grammar%20mistakes.',
      {
        headers: {
          'Authorization': 'Bearer test-api-key',
          'X-Request-ID': expect.any(String)
        }
      }
    );
  });

  it('should track user improvement', async () => {
    const mockResponse = { data: { corrected_text: 'This is a corrected sentence.' } };
    axios.get.mockResolvedValue(mockResponse);

    await api.correctGrammar('This is a sentence with grammar mistakes.');
    const history = api.getUserHistory('current_user_id');
    expect(history.length).toBe(1);
    expect(history[0].originalText).toBe('This is a sentence with grammar mistakes.');
    expect(history[0].correctedText).toBe('This is a corrected sentence.');
  });

  it('should handle errors', async () => {
    axios.get.mockRejectedValue(new Error('API request failed'));

    await expect(api.correctGrammar('This is a sentence with grammar mistakes.'))
      .rejects
      .toThrow('API request failed');
  });
});