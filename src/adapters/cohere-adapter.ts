import { BaseLLMAdapter, LLMRequest, LLMResponse } from './base-adapter';

export class CohereAdapter extends BaseLLMAdapter {
  private readonly API_URL = 'https://api.cohere.ai/v1/generate';

  constructor(apiKey: string) {
    super();
    this.setAuth(apiKey);
  }

  private setAuth(apiKey: string): void {
    this.headers = {
      ...this.headers,
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    };
  }

  async chatCompletion(request: LLMRequest): Promise<LLMResponse> {
    const cohereRequest = {
      model: request.model || 'command',
      prompt: this.formatMessagesToPrompt(request.messages),
      max_tokens: request.max_tokens || 150,
      temperature: request.temperature || 0.7,
      k: 0,
      p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
      stop_sequences: request.stop || [],
    };

    const response = await this.fetchWithRetry(this.API_URL, {
      method: 'POST',
      body: JSON.stringify(cohereRequest),
    });

    if (!response.ok) {
      throw new Error(`Cohere API error: ${await response.text()}`);
    }

    const data = await response.json();
    
    return {
      content: data.text.trim(),
      usage: {
        prompt_tokens: data.prompt_tokens,
        completion_tokens: data.generated_tokens,
        total_tokens: data.total_tokens,
      },
    };
  }

  private formatMessagesToPrompt(messages: { role: string; content: string }[]): string {
    return messages
      .map(msg => 
        msg.role === 'user' ? `User: ${msg.content}` : 
        msg.role === 'assistant' ? `Assistant: ${msg.content}` : 
        msg.content
      )
      .join('\n') + '\nAssistant:';
  }
}