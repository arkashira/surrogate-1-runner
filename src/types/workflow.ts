/* --------------------------------------------------------------
   Core workflow schema – the shape that is stored as JSON in DB.
   -------------------------------------------------------------- */

export type Primitive = 'string' | 'number' | 'boolean';
export type Complex   = 'object' | 'array';
export type InputType = Primitive | Complex;

/* ---------- INPUT / OUTPUT ---------- */
export interface WorkflowIO {
  /** Human‑readable name */
  name: string;
  /** Data type */
  type: InputType;
  /** Optional description */
  description?: string;
}

/** Input definition – may be required and have a default value */
export interface WorkflowInput extends WorkflowIO {
  required: boolean;
  /** Default value used when the input is omitted */
  default?: unknown;
}

/** Output definition – never has a default */
export interface WorkflowOutput extends WorkflowIO {}

/* ---------- STEPS ---------- */
export type StepType = 'task' | 'condition' | 'parallel' | 'transform';

export interface BaseStep {
  /** Unique identifier inside the workflow */
  id: string;
  /** Friendly name */
  name: string;
  /** Kind of step */
  type: StepType;
  /** Optional description */
  description?: string;
  /** Arbitrary key/value pairs that the step implementation consumes */
  inputs?: Record<string, unknown>;
  /** IDs of steps that must finish before this one starts */
  dependsOn?: string[];
  /** IDs of successor steps (used by visual editors) */
  next?: string[];
}

/** Transform‑specific configuration */
export interface TransformStep extends BaseStep {
  type: 'transform';
  transform: {
    /** map | filter | reduce */
    type: 'map' | 'filter' | 'reduce';
    /** Optional expression language (e.g. JS, JSONata) */
    expression?: string;
  };
}

/** Condition‑specific configuration */
export interface ConditionStep extends BaseStep {
  type: 'condition';
  condition: {
    field: string;
    operator:
      | 'eq'
      | 'ne'
      | 'gt'
      | 'lt'
      | 'gte'
      | 'lte'
      | 'contains'
      | 'in';
    value: unknown;
  };
}

/** Union of all concrete step shapes */
export type WorkflowStep = BaseStep | TransformStep | ConditionStep;

/* ---------- MAIN DEFINITION ---------- */
export interface WorkflowDefinition {
  /** Human‑readable name (must be unique across the system) */
  name: string;
  /** Long description */
  description: string;
  /** Semantic version, e.g. "1.0.0" */
  version: string;
  /** Input contract */
  inputs: WorkflowInput[];
  /** Execution graph */
  steps: WorkflowStep[];
  /** Output contract */
  outputs: WorkflowOutput[];
}

/* ---------- PERSISTED ENTITY ---------- */
export type WorkflowStatus = 'draft' | 'active' | 'deprecated' | 'archived';

export interface Workflow extends WorkflowDefinition {
  /** Primary key */
  id: string;
  /** Lifecycle state */
  status: WorkflowStatus;
  /** Auditing */
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}

/* ---------- VERSION HISTORY ---------- */
export interface WorkflowVersion {
  /** PK of the version row */
  id: string;
  /** FK → Workflow.id */
  workflowId: string;
  /** Version string (copied from definition.version) */
  version: string;
  /** Full snapshot of the definition at this point in time */
  definition: WorkflowDefinition;
  /** Human‑readable changelog */
  changelog?: string;
  /** Auditing */
  createdAt: Date;
  createdBy: string;
}

/* ---------- VALIDATION RESULT ---------- */
export type ValidationErrorCode =
  | 'MISSING_REQUIRED'
  | 'INVALID_TYPE'
  | 'INVALID_FORMAT'
  | 'CIRCULAR_DEPENDENCY'
  | 'INVALID_REFERENCE';

export type ValidationWarningCode =
  | 'UNUSED_INPUT'
  | 'UNREACHABLE_STEP'
  | 'UNUSED_OUTPUT';

export interface ValidationError {
  path: string; // JSON‑pointer like "steps[3].inputs.foo"
  message: string;
  code: ValidationErrorCode;
}

export interface ValidationWarning {
  path: string;
  message: string;
  code: ValidationWarningCode;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}