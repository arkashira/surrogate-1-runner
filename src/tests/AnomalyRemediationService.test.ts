import { AnomalyRemediationService } from '../services/AnomalyRemediationService';
import { TeamSyncService } from '../services/TeamSyncService';
import { AnomalyTicket } from '../models/AnomalyTicket';

describe('AnomalyRemediationService', () => {
  let anomalyRemediationService: AnomalyRemediationService;
  let mockTeamSyncService: jest.Mocked<TeamSyncService>;

  beforeEach(() => {
    mockTeamSyncService = {
      syncTicket: jest.fn(),
      getTicket: jest.fn(),
      updateTicket: jest.fn()
    } as unknown as jest.Mocked<TeamSyncService>;
    anomalyRemediationService = new AnomalyRemediationService(mockTeamSyncService);
  });

  it('should create a ticket and sync it across teams', async () => {
    const newTicket: AnomalyTicket = {
      id: 'ticket123',
      title: 'Cost Anomaly Detected',
      description: 'A significant cost anomaly has been detected in the system.',
      status: 'open',
      assignedTo: 'DevTeam'
    };
    await anomalyRemediationService.createTicket(newTicket);
    expect(mockTeamSyncService.syncTicket).toHaveBeenCalledWith(newTicket);
  });

  it('should view a ticket', async () => {
    const ticketId = 'ticket123';
    await anomalyRemediationService.viewTicket(ticketId);
    expect(mockTeamSyncService.getTicket).toHaveBeenCalledWith(ticketId);
  });

  it('should edit a ticket', async () => {
    const ticketId = 'ticket123';
    const updates = { status: 'in-progress' };
    await anomalyRemediationService.editTicket(ticketId, updates);
    expect(mockTeamSyncService.updateTicket).toHaveBeenCalledWith(ticketId, updates);
  });
});