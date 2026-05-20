import { OpenAIAdapter, Message, ChatResponse } from '../../src/adapters/openai-adapter';
import fetch from 'node-fetch';

jest.mock('node-fetch');
const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;

describe('OpenAIAdapter', () => {
  const dummyApiKey = 'sk-test';
  const adapter = new OpenAIAdapter(dummyApiKey);

  const sampleMessages: Message[] = [
    { role: 'user', content: 'Hello' },
  ];

  const sampleResponse: ChatResponse = {
    id: 'chatcmpl-123',
    object: 'chat.completion',
    created: 1690000000,
    model: 'gpt-3.5-turbo',
    choices: [
      {
        index: 0,
        message: { role: 'assistant', content: 'Hi there!' },
        finish_reason: 'stop',
      },
    ],
    usage: {
      prompt_tokens: 3,
      completion_tokens: 4,
      total_tokens: 7,
    },
  };

  beforeEach(() => {
    mockedFetch.mockReset();
  });

  it('sends correct request and returns parsed response', async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      statusText: 'OK',
      json: async () => sampleResponse,
    } as any);

    const result = await adapter.chat(sampleMessages);

    expect(mockedFetch).toHaveBeenCalledTimes(1);
    const callArgs = mockedFetch.mock.calls[0];
    expect(callArgs[0]).toBe('https://api.openai.com/v1/chat/completions');
    const fetchOptions = callArgs[1];
    expect(fetchOptions?.method).toBe('POST');
    expect(fetchOptions?.headers).toEqual({
      Authorization: `Bearer ${dummyApiKey}`,
      'Content-Type': 'application/json',
    });
    const body = JSON.parse(fetchOptions?.body as string);
    expect(body).toEqual({
      model: 'gpt-3.5-turbo',
      messages: sampleMessages,
    });

    expect(result).toEqual(sampleResponse);
  });

  it('throws error on non-200 response', async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: 'Unauthorized',
      text: async () => 'Unauthorized',
    } as any);

    await expect(adapter.chat(sampleMessages)).rejects.toThrow(
      /OpenAI API error: 401 Unauthorized - Unauthorized/
    );
  });
});