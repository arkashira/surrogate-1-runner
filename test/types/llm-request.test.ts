import { LlmInvokeRequestSchema } from '../../src/types/llm-request';

describe('LlmInvokeRequestSchema', () => {
  it('should validate a valid request', () => {
    const validRequest = {
      model: 'gpt-3.5-turbo',
      prompt: 'Hello, world!',
      temperature: 0.7,
    };
    expect(LlmInvokeRequestSchema.safeParse(validRequest).success).toBe(true);
  });

  it('should reject invalid temperature values', () => {
    const invalidTempRequest = {
      model: 'gpt-3.5-turbo',
      prompt: 'Test',
      temperature: 1.5,
    };
    expect(LlmInvokeRequestSchema.safeParse(invalidTempRequest).success).toBe(false);
  });

  it('should reject negative maxTokens', () => {
    const invalidMaxTokensRequest = {
      model: 'gpt-3.5-turbo',
      prompt: 'Test',
      maxTokens: -10,
    };
    expect(LlmInvokeRequestSchema.safeParse(invalidMaxTokensRequest).success).toBe(false);
  });
});