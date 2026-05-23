import { config } from '../config';
import { StreamingParser } from './streaming';
import { LegacyBatchParser } from './legacy';

export class Parser {
  private parser: StreamingParser | LegacyBatchParser;

  constructor() {
    const isStreamingEnabled = config.get('parser.streaming.enabled') ||
                              process.env.PARSER_STREAMING_ENABLED === 'true';

    this.parser = isStreamingEnabled ? new StreamingParser() : new LegacyBatchParser();
  }

  public parse(data: string): any {
    return this.parser.parse(data);
  }
}