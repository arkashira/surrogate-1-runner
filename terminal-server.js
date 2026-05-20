const fs = require('fs');
const path = require('path');

const POLICIES_FILE = '/opt/axentx/surrogate-1/db/policies.json';
const ACCESS_AUDIT_LOG = '/opt/axentx/surrogate-1/logs/access-audit.log';

class TerminalServer {
  constructor() {
    this.policies = this.loadPolicies();
  }

  loadPolicies() {
    try {
      const data = fs.readFileSync(POLICIES_FILE, 'utf8');
      return JSON.parse(data);
    } catch (err) {
      console.error('Error loading policies:', err);
      return {};
    }
  }

  validateCommand(userRole, command) {
    const policy = this.policies[userRole];
    if (!policy) {
      this.logAccessAttempt(userRole, command, false, 'No policy for role');
      return false;
    }

    if (policy.allowedCommands.includes(command)) {
      this.logAccessAttempt(userRole, command, true);
      return true;
    }

    this.logAccessAttempt(userRole, command, false, 'Command not allowed');
    return false;
  }

  logAccessAttempt(userRole, command, isAllowed, reason = '') {
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} - UserRole: ${userRole}, Command: ${command}, Allowed: ${isAllowed}, Reason: ${reason}\n`;

    fs.appendFile(ACCESS_AUDIT_LOG, logEntry, (err) => {
      if (err) {
        console.error('Error writing to access audit log:', err);
      }
    });
  }
}

module.exports = TerminalServer;