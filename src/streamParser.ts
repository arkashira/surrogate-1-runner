import { Readable } from 'stream';

export async function streamParser(stream: Readable): Promise<number> {
  let processedSize = 0;
  stream.on('data', (chunk) => {
    processedSize += chunk.length;
  });
  await new Promise((resolve) => {
    stream.on('end', resolve);
  });
  return processedSize;
}