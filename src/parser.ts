import { Transform } from 'stream';

export function streamParser() {
  return new Transform({
    transform(chunk, encoding, callback) {
      // Simulate parsing logic
      const parsedChunk = chunk.toString().toUpperCase();
      this.push(parsedChunk);
      callback();
    }
  });
}