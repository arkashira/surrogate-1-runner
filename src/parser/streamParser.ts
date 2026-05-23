import { Readable } from 'stream';
import { parseBatch } from './batchParser';

/**
 * Parses a Node.js Readable stream containing the same format as the batch parser.
 *
 * The implementation reads the stream into memory in chunks, concatenates them,
 * and delegates to the existing batch parser. This keeps the public API
 * unchanged while providing a convenient streaming entry point.
 *
 * @param readable - The input stream to parse.
 * @returns A promise that resolves to the same result type as `parseBatch`.
 */
export async function parseStream(readable: Readable): Promise<any> {
  const chunks: Buffer[] = [];
  for await (const chunk of readable) {
    chunks.push(chunk as Buffer);
  }
  const data = Buffer.concat(chunks).toString('utf8');
  return parseBatch(data);
}