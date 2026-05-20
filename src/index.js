const RBAC = require('./rbac-engine');

const rbac = new RBAC();

// Example usage:
const userRole = 'admin';
const userPermissions = rbac.validateUser(userRole);
console.log(userPermissions);

rbac.auditAccessChange(userRole, 'execute_command');