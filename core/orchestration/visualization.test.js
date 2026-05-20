const Visualization = require('./visualization.js');
const WebSocket = require('ws');

describe('Visualization', () => {
  let visualization;
  let mockWs;

  beforeEach(() => {
    visualization = new Visualization();
    mockWs = new WebSocket('ws://localhost:8080');
  });

  afterEach(() => {
    mockWs.close();
  });

  it('should handle agent status updates', async () => {
    await new Promise((resolve) => {
      mockWs.on('open', () => {
        mockWs.send(JSON.stringify({
          type: 'agent-status',
          agentId: 'agent1',
          status: 'running'
        }));
        resolve();
      });
    });

    expect(visualization.agents['agent1']).toBe('running');
  });

  it('should handle subagent status updates', async () => {
    await new Promise((resolve) => {
      mockWs.on('open', () => {
        mockWs.send(JSON.stringify({
          type: 'subagent-status',
          subagentId: 'subagent1',
          status: 'idle'
        }));
        resolve();
      });
    });

    expect(visualization.subagents['subagent1']).toBe('idle');
  });

  it('should broadcast state to connected clients', async () => {
    await new Promise((resolve) => {
      mockWs.on('open', () => {
        mockWs.send(JSON.stringify({
          type: 'agent-status',
          agentId: 'agent1',
          status: 'running'
        }));
        resolve();
      });
    });

    const receivedMessages = [];
    mockWs.on('message', (message) => receivedMessages.push(JSON.parse(message)));

    expect(receivedMessages.length).toBeGreaterThan(0);
    expect(receivedMessages[0].agents['agent1']).toBe('running');
  });
});