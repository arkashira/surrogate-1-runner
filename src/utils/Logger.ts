export interface Logger {
  info(message: string): void;
  error(message: string): void;
  // Add other logging methods as needed
}

export class ConsoleLogger implements Logger {
  info(message: string): void {
    console.log(`INFO: ${message}`);
  }

  error(message: string): void {
    console.error(`ERROR: ${message}`);
  }
}