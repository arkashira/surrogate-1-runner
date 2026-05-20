import { QuickJsEngine } from './QuickJsEngine';

describe('QuickJsEngine', () => {
  let engine: QuickJsEngine;

  beforeEach(() => {
    engine = new QuickJsEngine();
  });

  it('should execute a simple workflow', async () => {
    const workflowCode = '1 + 2';
    const result = await engine.executeWorkflow(workflowCode);
    expect(result).toBe(3);
  });

  it('should handle HTTP request action offline', async () => {
    const actionParams = { url: 'https://example.com' };
    await expect(engine.executeAction('httpRequest', actionParams)).rejects.toThrow('HTTP requests are not supported in offline mode.');
  });

  it('should simulate file read action', async () => {
    const actionParams = { path: '/path/to/file.txt' };
    const result = await engine.executeAction('fileRead', actionParams);
    expect(result).toBe('File content for /path/to/file.txt');
  });

  it('should simulate file write action', async () => {
    const actionParams = { path: '/path/to/file.txt', content: 'Hello, world!' };
    await engine.executeAction('fileWrite', actionParams);
    // No direct way to verify file write in test, just check if it doesn't throw
  });

  it('should simulate local DB query action', async () => {
    const actionParams = { query: 'SELECT * FROM table' };
    const result = await engine.executeAction('localDbQuery', actionParams);
    expect(result).toBe('Query result for SELECT * FROM table');
  });

  it('should log execution', async () => {
    const executionLogs = ['Log entry 1', 'Log entry 2'];
    await engine.logExecution(executionLogs);
    // No direct way to verify log storage in test, just check if it doesn't throw
  });
});