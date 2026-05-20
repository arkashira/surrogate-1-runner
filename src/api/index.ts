import { Dashboard, Alert } from '../types';

/**
 * In a real app replace these with `fetch('/api/dashboards')` etc.
 * The signatures stay the same, so the component never needs to change.
 */
export const getDashboards = async (): Promise<Dashboard[]> => [
  { id: 1, name: 'Dashboard 1' },
  { id: 2, name: 'Dashboard 2' },
];

export const getAlerts = async (): Promise<Alert[]> => [
  { id: 1, name: 'Alert 1' },
  { id: 2, name: 'Alert 2' },
];