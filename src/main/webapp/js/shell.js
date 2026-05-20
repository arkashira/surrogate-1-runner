document.addEventListener('DOMContentLoaded', () => {
    const terminalElement = document.getElementById('terminal');
    
    // Initialize xterm.js
    const term = new Terminal({
        rendererType: 'canvas',
        rows: 30,
        cols: 80,
        scrollback: 1000,
        cursorBlink: true
    });

    term.open(terminalElement);

    // WebSocket setup for real-time communication
    const socket = new WebSocket('ws://your-websocket-server.com/shell');

    socket.onopen = () => {
        console.log('WebSocket connection established.');
    };

    socket.onmessage = (event) => {
        term.write(event.data);
    };

    term.onData((data) => {
        socket.send(data);
    });
});