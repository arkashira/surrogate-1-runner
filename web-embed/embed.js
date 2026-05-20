(function() {
    const iframeSrc = 'https://your-websocket-endpoint.com/chat';
    const iframe = document.createElement('iframe');
    iframe.src = iframeSrc;
    iframe.style.position = 'fixed';
    iframe.style.bottom = '0';
    iframe.style.right = '0';
    iframe.style.width = '400px';
    iframe.style.height = '600px';
    iframe.style.border = 'none';
    document.body.appendChild(iframe);

    let socket;
    function connectWebSocket() {
        socket = new WebSocket('wss://your-websocket-endpoint.com');
        socket.onopen = function(event) {
            console.log('Connected to WebSocket server');
        };
        socket.onmessage = function(event) {
            console.log('Received message:', event.data);
        };
        socket.onclose = function(event) {
            console.log('WebSocket connection closed, reconnecting...');
            setTimeout(connectWebSocket, 5000);
        };
        socket.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }

    window.addEventListener('focus', () => {
        if (socket && socket.readyState !== WebSocket.OPEN) {
            connectWebSocket();
        }
    });

    connectWebSocket();
})();