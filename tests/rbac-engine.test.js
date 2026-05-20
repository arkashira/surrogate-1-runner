const RBAC = require('../src/rbac-engine');

describe('RBAC', () => {
  it('validates user permissions', () => {
    const rbac = new RBAC();
    const userRole = 'admin';
    const userPermissions = rbac.validateUser(userRole);
    expect(userPermissions).toBeInstanceOf(Array);
  });

  it('logs access changes', () => {
    const rbac = new RBAC();
    const userRole = 'admin';
    rbac.auditAccessChange(userRole, 'execute_command');
    const logEntry = rbac.getLogEntry();
    expect(logEntry).toHaveProperty('timestamp');
    expect(logEntry).toHaveProperty('userRole');
    expect(logEntry).toHaveProperty('action');
  });
});

// Helper function to read log entry from file
function getLogEntry() {
  const logPath = '/opt/axentx/surrogate-1/logs/access-audit/access-audit.log';
  const logEntry = fs.readFileSync(logPath, 'utf8').split('\n').pop();
  return JSON.parse(logEntry);
}