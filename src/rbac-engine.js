const fs = require('fs');
const path = require('path');

const policiesPath = '/opt/axentx/surrogate-1/db/policies.json';
const logsPath = '/opt/axentx/surrogate-1/logs/access-audit';

class RBAC {
  constructor() {
    this.policies = JSON.parse(fs.readFileSync(policiesPath, 'utf8'));
  }

  validateUser(userRole) {
    const userPermissions = this.policies[userRole];
    return userPermissions ? userPermissions : [];
  }

  auditAccessChange(userRole, action) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      userRole,
      action,
    };
    fs.appendFileSync(path.join(logsPath, 'access-audit.log'), JSON.stringify(logEntry) + '\n');
  }
}

module.exports = RBAC;