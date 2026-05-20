const fs = require('fs');
const TerminalServer = require('../terminal-server');

describe('TerminalServer', () => {
  beforeEach(() => {
    // Create a mock policies file
    const mockPolicies = {
      admin: { allowedCommands: ['ls', 'cd', 'rm'] },
      user: { allowedCommands: ['ls', 'cd'] }
    };
    fs.writeFileSync('/opt/axentx/surrogate-1/db/policies.json', JSON.stringify(mockPolicies));
  });

  afterEach(() => {
    // Clean up the mock policies file
    fs.unlinkSync('/opt/axentx/surrogate-1/db/policies.json');
    fs.unlinkSync('/opt/axentx/surrogate-1/logs/access-audit.log');
  });

  test('should validate allowed commands for admin role', () => {
    const terminalServer = new TerminalServer();
    expect(terminalServer.validateCommand('admin', 'ls')).toBe(true);
    expect(terminalServer.validateCommand('admin', 'cd')).toBe(true);
    expect(terminalServer.validateCommand('admin', 'rm')).toBe(true);
  });

  test('should reject commands not allowed for admin role', () => {
    const terminalServer = new TerminalServer();
    expect(terminalServer.validateCommand('admin', 'chmod')).toBe(false);
  });

  test('should validate allowed commands for user role', () => {
    const terminalServer = new TerminalServer();
    expect(terminalServer.validateCommand('user', 'ls')).toBe(true);
    expect(terminalServer.validateCommand('user', 'cd')).toBe(true);
  });

  test('should reject commands not allowed for user role', () => {
    const terminalServer = new TerminalServer();
    expect(terminalServer.validateCommand('user', 'rm')).toBe(false);
    expect(terminalServer.validateCommand('user', 'chmod')).toBe(false);
  });

  test('should log access attempts', () => {
    const terminalServer = new TerminalServer();
    terminalServer.validateCommand('admin', 'ls');
    terminalServer.validateCommand('user', 'cd');
    terminalServer.validateCommand('user', 'rm');

    const logContent = fs.readFileSync('/opt/axentx/surrogate-1/logs/access-audit.log', 'utf8');
    expect(logContent).toContain('UserRole: admin, Command: ls, Allowed: true');
    expect(logContent).toContain('UserRole: user, Command: cd, Allowed: true');
    expect(logContent).toContain('UserRole: user, Command: rm, Allowed: false');
  });
});