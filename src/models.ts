export interface Workflow {
  id: string;
  name: string;
  steps: Step[];
}

export interface Step {
  id: string;
  type: string;          // e.g., 'http', 'db', 'ui'
  config: Record<string, any>;
}

export interface StepResult {
  stepId: string;
  status: 'completed' | 'failed' | 'pending';
  data?: any;
  error?: string;
}