import { Readable } from 'stream';
import { parseStream } from '../src/parser/parseEntry';
import { Result } from '../src/parser/types';

describe('parseStream', () => {
  it('should parse a stream correctly', async () => {
    const testData = Buffer.from('test data');
    const readable = new Readable({
      read() {
        this.push(testData);
        this.push(null);
      },
    });

    const result = await parseStream(readable);

    expect(result).toEqual({
      // Expected result structure
    } as Result);
  });

  it('should handle errors gracefully', async () => {
    const readable = new Readable({
      read() {
        this.emit('error', new Error('Test error'));
      },
    });

    await expect(parseStream(readable)).rejects.toThrow('Test error');
  });
});