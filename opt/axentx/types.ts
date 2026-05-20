export interface Anomaly {
  id: string;
  team: string;
  project: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  type: string;
  timestamp: Date;
  details: string;
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
}

export interface RemediationAction {
  id: string; // Added unique identifier
  anomalyId: string;
  team: string;
  action: string;
  user: string;
  timestamp: Date;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  notes?: string; // Optional field for additional context
}