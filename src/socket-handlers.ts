import { Socket } from 'socket.io';
import { messageSentCounter, panelOpenCounter, panelSessionDuration } from './metrics';

export function handlePanelEvents(socket: Socket) {
  // 1. Track Panel Open
  socket.on('panel_open', () => {
    panelOpenCounter.inc();
    
    // Store the start time on the socket instance to track duration
    // We use socket.data to store custom state
    socket.data.panelStartTime = Date.now();
    console.log(`Panel opened: ${socket.id}`);
  });

  // 2. Track Panel Close (Calculate Duration)
  socket.on('panel_close', () => {
    if (socket.data.panelStartTime) {
      const durationMs = Date.now() - socket.data.panelStartTime;
      const durationSeconds = durationMs / 1000;
      
      // Observe the duration in the histogram
      panelSessionDuration.observe(durationSeconds);
      
      // Clean up
      delete socket.data.panelStartTime;
      console.log(`Panel closed: ${socket.id}, Duration: ${durationSeconds}s`);
    }
  });
}

export function handleMessageEvents(socket: Socket) {
  socket.on('message_sent', () => {
    // Increment the counter for every message
    messageSentCounter.inc();
    console.log(`Message sent by: ${socket.id}`);
  });
}