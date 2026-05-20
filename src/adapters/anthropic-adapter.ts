import axios, { AxiosInstance } from 'axios';

interface AnthropicConfig {
  apiKey: string;
}

interface AnthropicResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: {
    text: string;
    index: number;
    finish_reason: string;
  }[];
}

export class AnthropicAdapter {
  private api: AxiosInstance;

  constructor(config: AnthropicConfig) {
    this.api = axios.create({
      baseURL: 'https://api.anthropic.com/v1',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${config.apiKey}`,
      },
    });
  }

  public async chatCompletion(messages: { role: string; content: string }[]): Promise<string> {
    const response = await this.api.post<AnthropicResponse>('/chat/completions', {
      model: 'claude-2.1',
      messages,
      max_tokens: 100,
    });

    return response.data.choices[0].text.trim();
  }
}