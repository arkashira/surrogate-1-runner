import axios from 'axios';

class StreamParser {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl: string = 'https://api.surrogate-1.axentx.com') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  async streamData(shardId: number, limit: number = 1000, offset: number = 0) {
    const url = `${this.baseUrl}/stream?shard_id=${shardId}&limit=${limit}&offset=${offset}`;
    const response = await axios.get(url, {
      headers: {
        'X-API-Key': this.apiKey,
      },
      responseType: 'stream',
    });

    return response.data;
  }

  async parseStream(shardId: number, limit: number = 1000, offset: number = 0) {
    const stream = await this.streamData(shardId, limit, offset);
    let data = '';

    stream.on('data', (chunk) => {
      data += chunk;
    });

    stream.on('end', () => {
      console.log('Stream ended');
      const records = data.split('\n').filter(Boolean).map(JSON.parse);
      console.log('Parsed records:', records);
    });

    stream.on('error', (err) => {
      console.error('Stream error:', err);
    });
  }
}

// Example usage
const apiKey = 'your-api-key';
const streamParser = new StreamParser(apiKey);

streamParser.parseStream(1, 100, 0)
  .then(() => console.log('Stream parsing completed'))
  .catch((err) => console.error('Error:', err));