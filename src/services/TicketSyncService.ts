import { Ticket } from '../models/Ticket';
import { DevTeamClient } from '../clients/DevTeamClient';
import { SRETeamClient } from '../clients/SRETeamClient';
import { FinOpsTeamClient } from '../clients/FinOpsTeamClient';

export class TicketSyncService {
  private devTeamClient: DevTeamClient;
  private sreTeamClient: SRETeamClient;
  private finOpsTeamClient: FinOpsTeamClient;

  constructor() {
    this.devTeamClient = new DevTeamClient();
    this.sreTeamClient = new SRETeamClient();
    this.finOpsTeamClient = new FinOpsTeamClient();
  }

  async syncTicket(ticket: Ticket): Promise<void> {
    await this.devTeamClient.updateTicket(ticket);
    await this.sreTeamClient.updateTicket(ticket);
    await this.finOpsTeamClient.updateTicket(ticket);
  }

  async syncAllTickets(tickets: Ticket[]): Promise<void> {
    for (const ticket of tickets) {
      await this.syncTicket(ticket);
    }
  }
}

// Example usage
(async () => {
  const ticketSyncService = new TicketSyncService();
  const tickets = [/* array of Ticket objects */];
  await ticketSyncService.syncAllTickets(tickets);
})();