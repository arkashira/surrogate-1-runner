import fetch, { Response } from 'node-fetch';

export interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface ChatChoice {
  index: number;
  message: Message;
  finish_reason: string;
}

export interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: ChatChoice[];
  usage: Usage;
}

export class OpenAIAdapter {
  private readonly apiKey: string;
  private readonly endpoint = 'https://api.openai.com/v1/chat/completions';
  private readonly model = 'gpt-3.5-turbo';

  constructor(apiKey?: string) {
    this.apiKey = apiKey ?? process.env.OPENAI_API_KEY ?? '';
    if (!this.apiKey) {
      throw new Error('OpenAI API key is required');
    }
  }

  static fromEnv(): OpenAIAdapter {
    return new OpenAIAdapter(process.env.OPENAI_API_KEY);
  }

  async chat(messages: Message[]): Promise<ChatResponse> {
    const body = {
      model: this.model,
      messages,
    };

    const response: Response = await fetch(this.endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`OpenAI API error: ${response.status} ${response.statusText} - ${errorText}`);
    }

    const data = (await response.json()) as ChatResponse;
    return data;
  }
}