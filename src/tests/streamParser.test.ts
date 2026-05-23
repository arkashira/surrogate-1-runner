import { generateLargeStream } from './largeStreamGenerator';
import { streamParser } from '../src/streamParser';

describe('streamParser', () => {
  it('processes large stream without OOM and within acceptable throughput', async () => {
    const sizeMb = 2;
    const stream = generateLargeStream(sizeMb);

    const startTime = Date.now();
    const processedSize = await streamParser(stream);
    const endTime = Date.now();

    const processingTimePerMB = (endTime - startTime) / (sizeMb * 1024);
    expect(processingTimePerMB).toBeLessThanOrEqual(200); // 200 ms per MB
    expect(processedSize).toBe(sizeMb * 1024 * 1024);
  });
});