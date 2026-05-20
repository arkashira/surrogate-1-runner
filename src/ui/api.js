const WebSocket = require('ws');

function launchTerminal(nodeId) {
  const wsUrl = `wss://backend.example.com/ws/${nodeId}`;
  const ws = new WebSocket(wsUrl);

  ws.on('open', () => {
    console.log('WebSocket connection established');
    // Initialize xterm.js terminal here
  });

  ws.on('error', (error) => {
    console.error('WebSocket connection failed:', error);
    // Show user-friendly error with retry option
  });

  return ws;
}

module.exports = {
  launchTerminal,
};