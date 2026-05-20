// Define the structure for resource metadata used by the idle detector
export interface Resource {
  id: string;
  type: 'runner' | 'worker' | 'storage' | 'database';
  last_activity: number; // Unix timestamp in milliseconds
  status: 'active' | 'idle' | 'shutdown';
  creation_time: number;
  // Additional metadata can be added as needed
}