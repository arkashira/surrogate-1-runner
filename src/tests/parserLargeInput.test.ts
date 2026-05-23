import { Readable } from 'stream';
import { streamParser } from '../parser';
import { expect } from 'chai';

describe('Large Stream Parser', () => {
  it('should parse a 2GB stream without OOM and with acceptable throughput', async () => {
    // Create a 2GB readable stream
    const streamSize = 2 * 1024 * 1024 * 1024; // 2GB
    const chunkSize = 1024 * 1024; // 1MB chunks
    let bytesRead = 0;

    const stream = new Readable({
      read() {
        if (bytesRead >= streamSize) {
          this.push(null);
          return;
        }

        const chunk = Buffer.alloc(chunkSize, 'a');
        this.push(chunk);
        bytesRead += chunkSize;
      }
    });

    // Measure start time
    const startTime = process.hrtime();

    // Parse the stream
    const parser = streamParser();
    stream.pipe(parser);

    // Collect parsed data
    const parsedData: any[] = [];
    parser.on('data', (data) => {
      parsedData.push(data);
    });

    await new Promise((resolve) => {
      parser.on('end', resolve);
    });

    // Measure end time
    const endTime = process.hrtime(startTime);
    const elapsedTime = endTime[0] * 1000 + endTime[1] / 1e6; // Convert to milliseconds

    // Calculate throughput
    const throughput = elapsedTime / (streamSize / (1024 * 1024)); // ms per MB

    // Check throughput
    expect(throughput).to.be.lessThan(200);

    // Check memory usage
    const memoryUsage = process.memoryUsage();
    expect(memoryUsage.rss).to.be.lessThan(70 * 1024 * 1024); // 70MB in bytes

    // Check coverage
    // This is a simplified example; actual coverage would require more complex setup
    expect(parsedData.length).to.be.greaterThan(0);
  });
});