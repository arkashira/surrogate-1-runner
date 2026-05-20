const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const pty = require('node-pty');

const LOG_DIR = path.resolve(process.cwd(), 'web-terminal-logs');
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

class Session {
  constructor(user) {
    this.id = uuidv4();
    this.user = user;
    this.pty = pty.spawn(process.env.SHELL || 'bash', [], {
      name: 'xterm-color',
      cols: 80,
      rows: 30,
      cwd: process.env.HOME,
      env: process.env,
    });
    this.auditLogPath = path.join(LOG_DIR, `${this.id}.log`);
    this.logStream = fs.createWriteStream(this.auditLogPath, { flags: 'a' });
    this.isConnected = true;
  }

  auditLog(data) {
    const ts = new Date().toISOString();
    this.logStream.write(`[${ts}] ${data}\n`);
  }

  destroy() {
    this.pty.kill();
    this.logStream.end();
    this.isConnected = false;
  }
}

class SessionManager {
  constructor() {
    this.sessions = new Map(); // sessionId -> Session
    this.cleanupInterval = setInterval(() => {
      const now = Date.now();
      for (const [id, session] of this.sessions.entries()) {
        if (!session.isConnected && Date.now() - session.id > 60000) { // 1分钟无活动自动清理
          session.destroy();
          this.sessions.delete(id);
        }
      }
    }, 30000); // 每30秒检查一次
  }

  createSession(user) {
    const session = new Session(user);
    this.sessions.set(session.id, session);
    return session;
  }

  getSession(id) {
    return this.sessions.get(id);
  }

  deleteSession(id) {
    const session = this.sessions.get(id);
    if (session) {
      session.destroy();
      this.sessions.delete(id);
    }
  }

  cleanup() {
    clearInterval(this.cleanupInterval);
    this.sessions.forEach(session => session.destroy());
    this.sessions.clear();
  }
}

module.exports = {
  SessionManager,
};