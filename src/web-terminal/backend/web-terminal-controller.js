const { SessionManager } = require('./web-terminal-model');

const sessionManager = new SessionManager();

class WebTerminalController {
  constructor(model) {
    this.model = model;
  }

  async startSession(user) {
    const session = this.model.createSession(user);
    return { id: session.id, logPath: session.auditLogPath };
  }

  async stopSession(user, sessionId) {
    const session = this.model.getSession(sessionId);
    if (!session) throw new Error('Session not found');
    if (session.user.id !== user.id) throw new Error('Unauthorized');
    session.destroy();
    this.model.deleteSession(sessionId);
  }

  async attachClient(socket, sessionId) {
    const session = this.model.getSession(sessionId);
    if (!session) throw new Error('Session not found');

    // 前向客户端输入到终端
    socket.on('input', (data) => {
      session.pty.write(data);
      session.auditLog(`INPUT: ${data}`);
    });

    // 前向终端输出到客户端
    const onData = (data) => {
      socket.emit('output', data);
      session.auditLog(`OUTPUT: ${data}`);
    };
    session.pty.on('data', onData);

    // 处理客户端断开连接
    socket.on('disconnect', () => {
      session.pty.off('data', onData);
      session.destroy();
      this.model.deleteSession(sessionId);
    });

    // 处理终端退出
    session.pty.on('exit', (code, signal) => {
      socket.emit('exit', { code, signal });
      session.destroy();
      this.model.deleteSession(sessionId);
    });
  }
}

module.exports = { WebTerminalController };