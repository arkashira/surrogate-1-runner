export interface WorkflowStep {
  id: string;
  name: string;
  action: string;
  config?: Record<string, unknown>;
}

export interface WorkflowInput {
  name: string;
  type: string;
  required: boolean;
  default?: unknown;
}

export interface WorkflowOutput {
  name: string;
  type: string;
}

/** Payload used when a client creates a workflow */
export interface CreateWorkflowDto {
  name: string;
  description?: string;
  inputs: WorkflowInput[];
  steps: WorkflowStep[];
  outputs: WorkflowOutput[];
}

/** Payload used when a client updates a workflow */
export interface UpdateWorkflowDto {
  id: string;
  name?: string;
  description?: string;
  inputs?: WorkflowInput[];
  steps?: WorkflowStep[];
  outputs?: WorkflowOutput[];
}