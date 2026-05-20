export interface AlertState {
  threshold: number;          // 5 – 95
  notificationMethod: 'email' | 'in-app';
}