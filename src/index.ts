import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import { register } from './metrics';
import { handlePanelEvents, handleMessageEvents } from './socket-handlers';

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: '*' } // Allow connections for testing
});

// Expose Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (ex) {
    res.status(500).end(ex);
  }
});

// Health check
app.get('/health', (req, res) => res.send('OK'));

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  handlePanelEvents(socket);
  handleMessageEvents(socket);
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});