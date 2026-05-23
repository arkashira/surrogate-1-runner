export const config = {
  get(key: string): any {
    // Implement config getter logic
    const defaultConfig = {
      'parser.streaming.enabled': true
    };
    return defaultConfig[key] || process.env[key.toUpperCase()];
  }
};