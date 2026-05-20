const http = require('http');
const { app, projectEmitter } = require('./app');
const socketIo = require('socket.io');

const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: '*' } });

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);

  const onProjectCreated = (project) => socket.emit('projectCreated', project);
  projectEmitter.on('projectCreated', onProjectCreated);

  socket.on('disconnect', () => {
    projectEmitter.off('projectCreated', onProjectCreated);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server listening on ${PORT}`));