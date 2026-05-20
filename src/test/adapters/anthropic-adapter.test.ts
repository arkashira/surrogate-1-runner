import { AnthropicAdapter } from '../adapters/anthropic-adapter';

describe('AnthropicAdapter', () => {
  const apiKey = 'your_anthropic_api_key_here';
  const adapter = new AnthropicAdapter({ apiKey });

  it('should create an instance of AnthropicAdapter', () => {
    expect(adapter).toBeInstanceOf(AnthropicAdapter);
  });

  it('should generate a response for chat completion', async () => {
    const messages = [
      { role: 'user', content: 'Hello! How are you?' },
    ];
    const response = await adapter.chatCompletion(messages);
    expect(response).toBeDefined();
    expect(response).not.toBe('');
  });
});