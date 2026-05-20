// tests/terminal.test.js
const WebSocket = require('ws');

describe('Terminal', () => {
    let server;
    let client;

    beforeEach(() => {
        server = new WebSocket.Server({ port: 8765 });
        client = new WebSocket('ws://localhost:8765');
    });

    afterEach(() => {
        server.close();
        client.close();
    });

    it('should handle incoming messages', (done) => {
        client.on('message', (message) => {
            expect(message).toBe('Hello, world!');
            done();
        });

        client.send('Hello, world!');
    });
});