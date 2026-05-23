import { Readable } from 'stream';

function generateLargeStream(sizeMb: number): Readable {
  const chunkSize = 1024 * 1024; // 1MB chunks
  const totalChunks = Math.ceil(sizeMb * chunkSize);

  let currentChunk = 0;

  return new Readable({
    read() {
      if (currentChunk < totalChunks) {
        const chunk = Buffer.alloc(chunkSize, String.fromCharCode(currentChunk % 256));
        this.push(chunk);
        currentChunk++;
      } else {
        this.push(null); // Signal end of stream
      }
    },
  });
}

export { generateLargeStream };