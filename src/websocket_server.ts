import { createServer } from 'http';
import { Server as WebSocketServer } from 'ws';
import { InteractionBus, AgentInteraction } from './agent_interaction';

const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 8080;

export class WebSocketVisualizationServer {
  private httpServer: any;
  private wss: WebSocketServer;
  private interactionBus: InteractionBus;

  constructor() {
    this.interactionBus = InteractionBus.getInstance();
    this.httpServer = createServer();
    this.wss = new WebSocketServer({ server: this.httpServer });

    // Set up event listener
    this.interactionBus.onInteraction((interaction: AgentInteraction) => {
      this.broadcast(interaction);
    });

    // Health check endpoint
    this.httpServer.on('request', (req, res) => {
      if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok' }));
      } else {
        res.writeHead(404);
        res.end();
      }
    });
  }

  private broadcast(interaction: AgentInteraction): void {
    const payload = JSON.stringify({
      type: 'interaction',
      data: interaction
    });

    this.wss.clients.forEach((client) => {
      if (client.readyState === client.OPEN) {
        client.send(payload);
      }
    });
  }

  public start(): void {
    this.httpServer.listen(PORT, () => {
      console.log(`WebSocket server listening on port ${PORT}`);
    });
  }

  public stop(): void {
    this.wss.close();
    this.httpServer.close();
  }
}