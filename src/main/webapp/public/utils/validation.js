
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
  }
}

/**
 * Map a provider name to a test endpoint and request options.
 *
 * @param {string} provider - e.g. "openai"
 * @returns {{url: string, options: object}}
 */
function getValidationRequest(provider, validateEndpoint) {
  switch (provider.toLowerCase()) {
    case 'openai':
      return {
        url: validateEndpoint,
        options: {
          method: 'GET',
          headers: {
            Authorization: 'Bearer {apiKey}',
            'Content-Type': 'application/json',
          },
        },
      };
    // Future providers can be added here.
    default:
      throw new ValidationError(`Unsupported provider: ${provider}`);
  }
}

/**
 * Interprets HTTP status codes from the provider's test endpoint.
 *
 * @param {number} status
 * @returns {{valid: boolean, message: string}}
 */
function interpretResponseStatus(status) {
  switch (status) {
    case 200:
      return { valid: true, message: 'API key is valid.' };
    case 401:
      return { valid: false, message: 'Invalid API key.' };
    case 429:
      return { valid: false, message: 'API key limit exceeded.' };
    default:
      return {
        valid: false,
        message: `Unexpected response from provider (status ${status}).`,
      };
  }
}

/**
 * Validates an API key for a given LLM provider.
 *
 * @param {string} provider - Name of the LLM provider (e.g., "openai").
 * @param {string} apiKey   - The API key supplied by the user.
 * @param {function} validateEndpoint - A function that returns the validation endpoint for the given provider.
 * @returns {Promise<{valid: boolean, message: string}>}
 * @throws {ValidationError} on empty key or unsupported provider.
 */
async function validateApiKey(provider, apiKey, validateEndpoint) {
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim() === '') {
    throw new ValidationError('API key cannot be empty.');
  }

  const { url, options } = getValidationRequest(provider, validateEndpoint);

  // Use the global fetch (available in browsers and Node >=18 or via polyfill).
  const response = await fetch(url, options);
  return interpretResponseStatus(response.status);
}

/**
 * Returns instructions for getting API keys for a given provider.
 *
 * @param {string} provider - Name of the LLM provider (e.g., "openai").
 * @returns {string} - Instructions for getting API keys.
 */
function getProviderInstructions(provider) {
  const instructions = {
    openai: 'Get your OpenAI API key from https://platform.openai.com/account/api-keys',
    anthropic: 'Get your Anthropic API key from https://console.anthropic.com/settings/keys',
    // Add more providers as needed
  };

  return instructions[provider] || 'Please contact support for API key instructions';
}

// Export for consumption in UI components and for unit testing.
export { validateApiKey, ValidationError, getProviderInstructions };