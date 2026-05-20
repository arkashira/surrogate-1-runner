import { TicketSyncService } from '../services/TicketSyncService';
import { DevTeamClient } from '../clients/DevTeamClient';
import { SRETeamClient } from '../clients/SRETeamClient';
import { FinOpsTeamClient } from '../clients/FinOpsTeamClient';
import { Ticket } from '../models/Ticket';

describe('TicketSyncService', () => {
  let ticketSyncService: TicketSyncService;
  let devTeamClient: DevTeamClient;
  let sreTeamClient: SRETeamClient;
  let finOpsTeamClient: FinOpsTeamClient;

  beforeEach(() => {
    devTeamClient = new DevTeamClient();
    sreTeamClient = new SRETeamClient();
    finOpsTeamClient = new FinOpsTeamClient();
    ticketSyncService = new TicketSyncService();
  });

  it('should sync a single ticket', async () => {
    const ticket: Ticket = {
      id: '1',
      title: 'Test Ticket',
      description: 'This is a test ticket',
      status: 'open',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    jest.spyOn(devTeamClient, 'updateTicket').mockResolvedValue(undefined);
    jest.spyOn(sreTeamClient, 'updateTicket').mockResolvedValue(undefined);
    jest.spyOn(finOpsTeamClient, 'updateTicket').mockResolvedValue(undefined);

    await ticketSyncService.syncTicket(ticket);

    expect(devTeamClient.updateTicket).toHaveBeenCalledWith(ticket);
    expect(sreTeamClient.updateTicket).toHaveBeenCalledWith(ticket);
    expect(finOpsTeamClient.updateTicket).toHaveBeenCalledWith(ticket);
  });

  it('should sync multiple tickets', async () => {
    const tickets: Ticket[] = [
      {
        id: '1',
        title: 'Test Ticket 1',
        description: 'This is a test ticket 1',
        status: 'open',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: '2',
        title: 'Test Ticket 2',
        description: 'This is a test ticket 2',
        status: 'open',
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];

    jest.spyOn(devTeamClient, 'updateTicket').mockResolvedValue(undefined);
    jest.spyOn(sreTeamClient, 'updateTicket').mockResolvedValue(undefined);
    jest.spyOn(finOpsTeamClient, 'updateTicket').mockResolvedValue(undefined);

    await ticketSyncService.syncAllTickets(tickets);

    expect(devTeamClient.updateTicket).toHaveBeenCalledTimes(2);
    expect(sreTeamClient.updateTicket).toHaveBeenCalledTimes(2);
    expect(finOpsTeamClient.updateTicket).toHaveBeenCalledTimes(2);
  });
});