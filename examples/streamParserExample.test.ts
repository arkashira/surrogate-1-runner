import { StreamParser } from './streamParserExample';
import axios from 'axios';
import { Readable } from 'stream';

jest.mock('axios');

describe('StreamParser', () => {
  const apiKey = 'test-api-key';
  const baseUrl = 'https://api.surrogate-1.axentx.com';
  const streamParser = new StreamParser(apiKey, baseUrl);

  it('should stream data', async () => {
    const mockData = JSON.stringify({ id: '1', data: 'record1' }) + '\n' +
                     JSON.stringify({ id: '2', data: 'record2' }) + '\n';
    const mockStream = new Readable();
    mockStream.push(mockData);
    mockStream.push(null);

    (axios.get as jest.Mock).mockResolvedValue({ data: mockStream });

    const stream = await streamParser.streamData(1, 100, 0);
    expect(axios.get).toHaveBeenCalledWith(`${baseUrl}/stream?shard_id=1&limit=100&offset=0`, {
      headers: { 'X-API-Key': apiKey },
      responseType: 'stream',
    });

    let data = '';
    stream.on('data', (chunk) => {
      data += chunk;
    });

    await new Promise((resolve) => {
      stream.on('end', resolve);
    });

    expect(data).toBe(mockData);
  });

  it('should parse stream', async () => {
    const mockData = JSON.stringify({ id: '1', data: 'record1' }) + '\n' +
                     JSON.stringify({ id: '2', data: 'record2' }) + '\n';
    const mockStream = new Readable();
    mockStream.push(mockData);
    mockStream.push(null);

    (axios.get as jest.Mock).mockResolvedValue({ data: mockStream });

    const consoleSpy = jest.spyOn(console, 'log');
    await streamParser.parseStream(1, 100, 0);

    expect(consoleSpy).toHaveBeenCalledWith('Stream ended');
    expect(consoleSpy).toHaveBeenCalledWith('Parsed records:', [
      { id: '1', data: 'record1' },
      { id: '2', data: 'record2' },
    ]);
    expect(consoleSpy).toHaveBeenCalledWith('Stream parsing completed');

    consoleSpy.mockRestore();
  });
});