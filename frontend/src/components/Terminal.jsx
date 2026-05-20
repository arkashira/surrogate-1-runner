import React, { useState, useEffect } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
import { WebSocket } from 'ws';

const TerminalComponent = () => {
  const [terminal, setTerminal] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080');
    const term = new Terminal({
      rows: 24,
      cols: 80,
      cursorBlink: true,
    });

    term.open(document.getElementById('terminal'));
    term.focus();

    ws.onopen = () => {
      setConnectionStatus('connected');
    };

    ws.onmessage = (event) => {
      term.write(event.data);
    };

    ws.onerror = () => {
      setConnectionStatus('error');
    };

    ws.onclose = () => {
      setConnectionStatus('disconnected');
    };

    setTerminal(term);

    return () => {
      ws.close();
    };
  }, []);

  const handleKeyPress = (event) => {
    if (event.ctrlKey && event.key === 'c') {
      // Handle Ctrl-C
    } else if (event.ctrlKey && event.key === 'z') {
      // Handle Ctrl-Z
    } else if (event.key === 'Tab') {
      // Handle tab completion
    }
  };

  const handleLogout = () => {
    // Clear JWT and close WebSocket
    localStorage.removeItem('jwt');
    terminal.dispose();
  };

  return (
    <div>
      <div id="terminal" />
      <p>Connection Status: {connectionStatus}</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default TerminalComponent;