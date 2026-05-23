import { Parser } from './parser';
import { getMemoryUsage } from './memoryService';
import { captureCrashLog } from './errorService';

export class ParserManager {
  private parsers: Parser[] = [];

  public addParser(parser: Parser): void {
    this.parsers.push(parser);
    setInterval(() => this.checkParserHealth(parser), 5000);
  }

  private checkParserHealth(parser: Parser): void {
    const memoryUsage = getMemoryUsage(parser);
    if (memoryUsage > 80) {
      console.warn(`Parser ${parser.id} is using high memory: ${memoryUsage}%`);
    }
  }
}