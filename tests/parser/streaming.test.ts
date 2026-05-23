import { parse } from '../parser';
import { createReadStream } from 'fs';
import { promisify } from 'util';
import { pipeline } from 'stream/promises';

describe('Streaming Parser', () => {
  const largeFilePath = '/path/to/large/synthetic/file.txt'; // Placeholder for the actual large file path

  it('should parse a large file using constant memory', async () => {
    const readStream = createReadStream(largeFilePath);
    const parsePromise = promisify(parse);

    await expect(async () => {
      await pipeline(readStream, parsePromise);
    }).resolves.not.toThrow();

    // Assuming there's a way to measure memory usage during execution
    expect(memoryUsage()).toBeLessThanOrEqual(100 * 1024 * 1024); // 100 MB
  });

  it('should not throw OOM or uncaught exceptions', async () => {
    const readStream = createReadStream(largeFilePath);
    const parsePromise = promisify(parse);

    await expect(async () => {
      await pipeline(readStream, parsePromise);
    }).resolves.not.toThrow();
  });

  it('should achieve throughput >= 50 MB/s', async () => {
    const readStream = createReadStream(largeFilePath);
    const parsePromise = promisify(parse);

    const startTime = Date.now();
    await pipeline(readStream, parsePromise);
    const endTime = Date.now();

    const fileSizeInBytes = 1024 * 1024 * 1024; // 1 GB file size
    const throughputInMBps = (fileSizeInBytes / 1024 / 1024) / ((endTime - startTime) / 1000);

    expect(throughputInMBps).toBeGreaterThanOrEqual(50);
  });
});

function memoryUsage() {
  // Placeholder function to simulate memory usage measurement
  return process.memoryUsage().heapUsed;
}