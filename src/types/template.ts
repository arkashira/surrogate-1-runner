export enum TemplateCategory {
  DataIngest = 'data-ingest',
  DataProcessing = 'data-processing',
  ModelTraining = 'model-training',
  Evaluation = 'evaluation',
  Deployment = 'deployment',
  Monitoring = 'monitoring',
}

export type ParameterType = 'string' | 'number' | 'boolean' | 'select' | 'array';

export interface TemplateParameter {
  name: string;
  type: ParameterType;
  label: string;
  description: string;
  defaultValue: string | number | boolean | string[];
  required: boolean;
  options?: string[]; // only for `select`
}

export interface TriggerConfig {
  type: 'schedule' | 'manual' | 'webhook';
  schedule?: string; // cron expression – required when type === 'schedule'
}

export interface WorkflowSettings {
  timeout: number;
  retries: number;
  environment?: string;
}

export interface WorkflowStep {
  id: string;
  name: string;
  action: string;
  config: Record<string, unknown>;
}

export interface WorkflowDefinition {
  steps: WorkflowStep[];
  triggers: TriggerConfig;
  settings: WorkflowSettings;
}

export interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  category: TemplateCategory;
  tags: string[];
  version: string;
  lastUpdated: string; // ISO‑8601
  author: string;
  parameters: TemplateParameter[];
  workflowDefinition: WorkflowDefinition;
}

export interface ImportedWorkflow extends WorkflowTemplate {
  importedAt: string; // ISO‑8601
  importedBy: string; // user id / email
  originalTemplateId: string;
  customName: string;
  parameterValues: Record<string, string | number | boolean | string[]>;
}