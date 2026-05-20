/**
 * Mock API key validation service.
 *
 * This module provides a client‑side mock for validating API keys against
 * selected LLM providers. It performs basic checks (empty key, length,
 * provider‑specific prefix) and returns a promise that resolves with a
 * validation result. The implementation is intentionally simple so that
 * it can be replaced with a real backend call in the future.
 *
 * Exported API:
 *   - validateApiKey(provider: string, key: string) -> Promise<{valid: boolean, error?: string}>
 *   - getProviderInstructions(provider: string) -> string
 */

const PROVIDER_PREFIXES = {
  openai: 'sk-',
  anthropic: 'anthropic-',
  cohere: 'cohere-',
};

const PROVIDER_MIN_KEY_LENGTH = {
  openai: 20,
  anthropic: 20,
  cohere: 20,
};

/**
 * Returns user‑friendly instructions for obtaining a valid key for the
 * specified provider.
 *
 * @param {string} provider
 * @returns {string}
 */
export function getProviderInstructions(provider) {
  switch (provider) {
    case 'openai':
      return 'Get an OpenAI API key from https://platform.openai.com/account/api-keys.';
    case 'anthropic':
      return 'Get an Anthropic API key from https://console.anthropic.com/account/api-keys.';
    case 'cohere':
      return 'Get a Cohere API key from https://dashboard.cohere.com/api-keys.';
    default:
      return 'Please provide a valid API key for the selected provider.';
  }
}

/**
 * Mock validation of an API key.
 *
 * The function performs the following checks in order:
 *   1. Empty key → error.
 *   2. Unsupported provider → error.
 *   3. Key length < minimum → error.
 *   4. Key does not start with expected provider prefix → error.
 *   5. Otherwise → success.
 *
 * @param {string} provider - The LLM provider identifier (e.g., 'openai').
 * @param {string} key - The API key to validate.
 * @returns {Promise<{valid: boolean, error?: string}>}
 */
export function validateApiKey(provider, key) {
  return new Promise((resolve) => {
    // 1. Empty key check
    if (!key || key.trim() === '') {
      return resolve({
        valid: false,
        error: 'API key cannot be empty.',
      });
    }

    // 2. Unsupported provider
    if (!PROVIDER_PREFIXES[provider]) {
      return resolve({
        valid: false,
        error: `Unsupported provider: ${provider}.`,
      });
    }

    const trimmedKey = key.trim();
    const minLength = PROVIDER_MIN_KEY_LENGTH[provider] || 20;
    const expectedPrefix = PROVIDER_PREFIXES[provider];

    // 3. Minimum length check
    if (trimmedKey.length < minLength) {
      return resolve({
        valid: false,
        error: 'API key is too short.',
      });
    }

    // 4. Prefix check
    if (!trimmedKey.startsWith(expectedPrefix)) {
      return resolve({
        valid: false,
        error: `Invalid ${provider} key format.`,
      });
    }

    // 5. Success
    return resolve({
      valid: true,
    });
  });
}