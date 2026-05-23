import { Readable } from 'stream';
import { Parser } from './index';

interface StreamingParserOptions {
  chunkSize: number;
}

export class StreamingParser extends Parser {
  private chunkSize: number;
  private input: Readable;
  private buffer: Buffer[] = [];
  private reading = false;

  constructor(options: StreamingParserOptions, input: Readable) {
    super();
    this.chunkSize = options.chunkSize;
    this.input = input;
  }

  private async readChunk() {
    if (this.reading) return;
    this.reading = true;
    const chunk = await new Promise<Buffer>((resolve, reject) => {
      this.input.once('data', resolve);
      this.input.once('error', reject);
    });
    this.buffer.push(chunk);
    this.reading = false;
  }

  async parse(): Promise<void> {
    while (this.buffer.length === 0) {
      await this.readChunk();
    }
    // Process buffered chunks here
  }
}