export interface Task {
  id: string;
  name: string;
  status: 'Running' | 'Completed';
  dataSize: string;
}