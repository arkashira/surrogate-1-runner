import { ParserManager } from '../nanocoder/parserManager';

const parserManager = new ParserManager();

export async function getParserHealth(): Promise<any> {
  const healthStatus = parserManager.parsers.map(parser => ({
    id: parser.id,
    memoryUsage: getMemoryUsage(parser),
    isRunning: parser.isRunning(),
  }));
  return healthStatus;
}