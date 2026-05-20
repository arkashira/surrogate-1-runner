import { io } from 'socket.io-client';

const SOCKET_SERVER_URL = 'https://api.axentx.com';

export const initRealTimeUpdates = (callback) => {
  const socket = io(SOCKET_SERVER_URL);

  socket.on('connect', () => {
    console.log('Connected to real-time updates server');
  });

  socket.on('onboardingDataUpdate', (data) => {
    callback(data);
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from real-time updates server');
  });

  return socket;
};