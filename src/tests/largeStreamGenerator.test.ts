import { generateLargeStream } from './largeStreamGenerator';

describe('Large Stream Generator', () => {
  it('should generate a readable stream of the specified size', async () => {
    const sizeMb = 2;
    const stream = generateLargeStream(sizeMb);

    let bytesRead = 0;
    await new Promise((resolve, reject) => {
      stream.on('data', (chunk) => {
        bytesRead += chunk.length;
      });

      stream.on('end', () => {
        expect(bytesRead).toBe(sizeMb * 1024 * 1024);
        resolve();
      });

      stream.on('error', reject);
    });
  });
});