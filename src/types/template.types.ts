export type TemplateCategory =
  | "data-ingest"
  | "data-processing"
  | "model-training"
  | "evaluation"
  | "deployment"
  | "monitoring"
  | "custom";

export interface ParameterValidation {
  min?: number;
  max?: number;
  pattern?: string;
  enum?: unknown[];
}

export interface TemplateParameter {
  name: string;
  type: "string" | "number" | "boolean" | "array" | "object";
  required: boolean;
  defaultValue?: unknown;
  description: string;
  validation?: ParameterValidation;
}

/** The *runtime* definition of a workflow – stored as JSON */
export interface WorkflowDefinition {
  steps: WorkflowStep[];
  dependencies: Record<string, string[]>;
}
export interface WorkflowStep {
  id: string;
  name: string;
  action: string;
  config: Record<string, unknown>;
}

/** Full DB‑entity shape (mirrors the TypeORM entity) */
export interface WorkflowTemplate {
  id: string;
  name: string;
  description?: string;
  category: TemplateCategory;
  tags?: string[];
  /** Numeric version for ordering (auto‑increment) */
  version: number;
  /** Human‑readable semver (e.g. "1.0.0") */
  semver: string;
  createdAt: Date;
  updatedAt: Date;
  /** Full workflow definition */
  workflowDefinition: WorkflowDefinition;
  /** Optional parameter catalogue */
  parameters?: TemplateParameter[];
}

/** DTO for importing a template */
export interface TemplateImportRequest {
  /** New name for the copy – required because the copy must be unique */
  name: string;
  /** Optional description */
  description?: string;
  /** Override tags (replaces the whole array) */
  tags?: string[];
  /** Override parameters (partial) */
  parameters?: Partial<TemplateParameter>[];
  /** Arbitrary overrides that will be merged into the workflowDefinition */
  workflowOverrides?: Partial<WorkflowDefinition>;
}

/** DTO for list queries */
export interface TemplateListQuery {
  category?: TemplateCategory;
  tags?: string[];
  search?: string; // matches name/description
  limit?: number;
  offset?: number;
}

/** Generic pagination wrapper */
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  limit: number;
  offset: number;
}