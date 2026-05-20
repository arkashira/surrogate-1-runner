import { Anomaly, RemediationAction } from '../types';

class RemediationLogService {
  private remediationHistory: RemediationAction[] = [];
  private databasePersistence: boolean = false;

  constructor(databasePersistence: boolean = false) {
    this.databasePersistence = databasePersistence;
  }

  async logRemediation(action: RemediationAction): Promise<void> {
    this.remediationHistory.push(action);
    if (this.databasePersistence) {
      // In a real implementation, persist to database
      await this.persistToDatabase(action);
    }
  }

  private async persistToDatabase(action: RemediationAction): Promise<void> {
    // Database persistence implementation
  }

  getRemediationHistory(): RemediationAction[] {
    return [...this.remediationHistory]; // Return copy to prevent mutation
  }

  getRemediationHistoryByAnomaly(anomalyId: string): RemediationAction[] {
    return this.remediationHistory.filter(action => action.anomalyId === anomalyId);
  }

  getRemediationHistoryByTeam(team: string): RemediationAction[] {
    return this.remediationHistory.filter(action => action.team === team);
  }

  getRemediationHistoryByStatus(status: RemediationAction['status']): RemediationAction[] {
    return this.remediationHistory.filter(action => action.status === status);
  }
}

export const remediationLogService = new RemediationLogService();