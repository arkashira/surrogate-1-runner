export enum Severity {
  Critical = 'critical',
  Warning = 'warning',
  Info = 'info',
}

export interface Alert {
  title: string;
  source: string;
  timestamp: string;
  affectedService: string;
  severity: Severity;
}