import { createHash } from 'crypto';

const parserGuardEnabled = process.env.PARSER_GUARD_ENABLED === 'true';

let parserCount = 0;

export function registerParser(type: 'json' | 'xml') {
  if (parserGuardEnabled) {
    parserCount++;
    if (parserCount > 1) {
      console.error(`Error: More than one ${type} parser detected. Aborting execution.`);
      process.exit(1);
    }
  }
}