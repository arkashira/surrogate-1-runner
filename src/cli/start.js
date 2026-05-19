const { spawn } = require('child_process');
const fs = require('fs');
const net = require('net');
const port = process.env.PORT || 3000;

const server = net.createServer();

server.listen(port, () => {
  console.log(`Sandbox URL: http://localhost:${port}`);
  const pid = process.pid;
  fs.writeFileSync('surrogate-1.pid', pid.toString());
  console.log(`PID file written: surrogate-1.pid`);
});

process.on('SIGTERM', () => {
  server.close();
  process.exit(0);
});

process.on('SIGINT', () => {
  server.close();
  process.exit(0);
});