import { LlmInvokeResponseSchema } from '../../src/types/llm-response';

describe('LlmInvokeResponseSchema', () => {
  it('should validate a successful response with metadata', () => {
    const successResponse = {
      model: 'gpt-4',
      content: 'The answer is 42.',
      metadata: {
        tokensUsed: 8,
        modelVersion: 'gpt-4-1106-preview'
      }
    };
    expect(LlmInvokeResponseSchema.safeParse(successResponse).success).toBe(true);
  });

  it('should reject content when there is an error', () => {
    const invalidResponse = {
      model: 'claude-3',
      content: 'This should be empty',
      error: {
        message: 'API rate limit exceeded',
        code: 'rate_limit',
      },
    };
    expect(LlmInvokeResponseSchema.safeParse(invalidResponse).success).toBe(false);
  });
});