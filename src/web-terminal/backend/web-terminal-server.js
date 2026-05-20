const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const bodyParser = require('body-parser');
const { WebTerminalController } = require('./web-terminal-controller');
const { WebTerminalModel } = require('./web-terminal-model');

const app = express();
app.use(bodyParser.json());

// SAML认证中间件（生产环境需实现实际验证）
app.use((req, res, next) => {
  try {
    // 模拟SAML验证 - 实际应用需替换为真实SAML处理
    const samlAssertion = req.headers['saml-assertion'];
    if (!samlAssertion) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    // 解析SAML并验证（示例：简单用户模拟）
    const user = {
      id: 'user_' + Date.now(),
      name: 'Authenticated User',
      email: 'user@example.com'
    };
    req.user = user;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid SAML assertion' });
  }
});

const controller = new WebTerminalController(new WebTerminalModel());

app.post('/api/terminal/start', async (req, res) => {
  try {
    const session = await controller.startSession(req.user);
    res.json({ sessionId: session.id });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/terminal/stop', async (req, res) => {
  try {
    await controller.stopSession(req.user, req.body.sessionId);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST'],
    allowedHeaders: ['*'],
  },
  pingInterval: 20000,
  pingTimeout: 5000,
});

io.on('connection', (socket) => {
  console.log('WebSocket client connected:', socket.id);
  socket.on('join', async ({ sessionId }) => {
    try {
      await controller.attachClient(socket, sessionId);
    } catch (err) {
      socket.emit('error', err.message);
      socket.disconnect(true);
    }
  });
});

const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.log(`Web terminal server listening on port ${PORT}`);
});