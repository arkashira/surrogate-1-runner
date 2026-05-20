/**
 * Tests for the mock API key validation service.
 *
 * These tests cover all validation branches and ensure that the
 * service behaves as expected for supported providers.
 */

import { validateApiKey, getProviderInstructions } from './api-validator';

describe('API Validator', () => {
  test('empty key returns error', async () => {
    const result = await validateApiKey('openai', '');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('API key cannot be empty.');
  });

  test('unsupported provider returns error', async () => {
    const result = await validateApiKey('unknown', 'sk-123456');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('Unsupported provider: unknown.');
  });

  test('key too short returns error', async () => {
    const result = await validateApiKey('openai', 'sk-123');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('API key is too short.');
  });

  test('invalid prefix returns error', async () => {
    const result = await validateApiKey('openai', 'invalid-12345678901234567890');
    expect(result.valid).toBe(false);
    expect(result.error).toBe('Invalid openai key format.');
  });

  test('valid key returns success', async () => {
    const result = await validateApiKey('openai', 'sk-12345678901234567890');
    expect(result.valid).toBe(true);
    expect(result.error).toBeUndefined();
  });

  test('instructions are returned for known provider', () => {
    const instr = getProviderInstructions('openai');
    expect(instr).toContain('OpenAI');
  });

  test('instructions fallback for unknown provider', () => {
    const instr = getProviderInstructions('unknown');
    expect(instr).toBe('Please provide a valid API key for the selected provider.');
  });
});