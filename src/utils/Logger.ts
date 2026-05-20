export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

export class Logger {
  private name: string;
  private minLevel: LogLevel;

  constructor(name: string, minLevel: LogLevel = LogLevel.INFO) {
    this.name = name;
    this.minLevel = minLevel;
  }

  private log(level: LogLevel, message: string, meta?: object) {
    if (level < this.minLevel) return;
    
    const timestamp = new Date().toISOString();
    const levelStr = LogLevel[level];
    const metaStr = meta ? ` ${JSON.stringify(meta)}` : '';
    
    console.log(`[${timestamp}] [${levelStr}] [${this.name}] ${message}${metaStr}`);
  }

  debug(message: string, meta?: object) {
    this.log(LogLevel.DEBUG, message, meta);
  }

  info(message: string, meta?: object) {
    this.log(LogLevel.INFO, message, meta);
  }

  warn(message: string, meta?: object) {
    this.log(LogLevel.WARN, message, meta);
  }

  error(message: string, meta?: object) {
    this.log(LogLevel.ERROR, message, meta);
  }
}