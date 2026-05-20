const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

class Visualization {
  constructor() {
    this.wsServer = new WebSocket.Server({ port: 8080 });
    this.agents = {};
    this.subagents = {};
    this.connections = {};

    this.wsServer.on('connection', (ws) => {
      const connectionId = uuidv4();
      this.connections[connectionId] = ws;
      ws.on('message', (message) => this.handleMessage(connectionId, message));
      ws.on('close', () => delete this.connections[connectionId]);
    });
  }

  handleMessage(connectionId, message) {
    const data = JSON.parse(message);
    switch (data.type) {
      case 'agent-status':
        this.updateAgentStatus(data.agentId, data.status);
        break;
      case 'subagent-status':
        this.updateSubagentStatus(data.subagentId, data.status);
        break;
      default:
        console.log('Unknown message type:', data.type);
    }
    this.broadcastState();
  }

  updateAgentStatus(agentId, status) {
    this.agents[agentId] = status;
  }

  updateSubagentStatus(subagentId, status) {
    this.subagents[subagentId] = status;
  }

  broadcastState() {
    const state = {
      agents: this.agents,
      subagents: this.subagents,
    };
    Object.values(this.connections).forEach((ws) => {
      ws.send(JSON.stringify(state));
    });
  }
}

module.exports = new Visualization();