export type Severity = 'critical' | 'warning' | 'info';

export interface Alert {
  id: string;
  message: string;
  timestamp: Date;
}

export interface AlertGroup {
  id: string;
  title: string;
  service: string;
  severity: Severity;
  alertCount: number;
  firstSeen: Date;
  lastSeen: Date;
  memberAlerts: Alert[];
}