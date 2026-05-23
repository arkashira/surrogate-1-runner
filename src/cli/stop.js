#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PID_FILE = path.join(__dirname, '../../run/surrogate-1.pid');

/**
 * Stops the surrogate-1 server by sending a SIGTERM signal.
 */
function stopServer() {
  try {
    // Read the PID from the PID file
    const pid = fs.readFileSync(PID_FILE, 'utf8').trim();
    
    // Log the action being taken
    console.log(`Stopping surrogate-1 server with PID ${pid}...`);
    
    // Send SIGTERM to the process
    process.kill(parseInt(pid), 'SIGTERM');
    
    // Wait for the process to exit gracefully
    setTimeout(() => {
      try {
        // Check if the process is still running
        process.kill(parseInt(pid), 0);
        console.error('Server did not stop gracefully. Forcing termination...');
        process.kill(parseInt(pid), 'SIGKILL');
      } catch (err) {
        // If the process does not exist, it means it has been terminated
        fs.unlinkSync(PID_FILE);
        console.log('Server stopped successfully.');
        process.exit(0);
      }
    }, 5000); // Wait for 5 seconds before checking again
    
  } catch (err) {
    // Handle errors appropriately with user feedback
    console.error('Error:', err.message);
    process.exit(1);
  }
}

stopServer();