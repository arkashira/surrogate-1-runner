/** Severity levels for a detected issue */
export enum Severity {
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
  HINT = 'hint',
}

/** High‑level categories – useful for aggregation & recommendations */
export enum IssueCategory {
  ANY_TYPE = 'any-type',
  IMPLICIT_ANY = 'implicit-any',
  TYPE_IGNORES = 'type-ignores',
  COMPLEX_TYPES = 'complex-types',
  UNSAFE_CASTS = 'unsafe-casts',
  OPTIONAL_CHAINING = 'optional-chaining',
  NULL_UNDEFINED = 'null-undefined',
  UNDEFINED_MEMBER = 'undefined-member',
}

/** One concrete problem found in the source */
export interface TypeIssue {
  id: string;                     // UUID or short hash
  file: string;                   // absolute or relative path
  line: number;                   // 1‑based
  column: number;                 // 1‑based
  severity: Severity;
  category: IssueCategory;
  message: string;                // human readable description
  code?: string;                  // TS error code (if any)
  suggestion?: string;           // quick‑fix hint
  impact: 'compilation-speed' | 'maintainability' | 'both';
}

/** Aggregated numbers for a whole run */
export interface ReportSummary {
  totalIssues: number;
  bySeverity: Record<Severity, number>;
  byCategory: Record<IssueCategory, number>;
  filesAffected: number;
  compilationSpeedImpact: number;
  maintainabilityImpact: number;
}

/** Per‑file slice of the report */
export interface FileReport {
  file: string;
  issues: TypeIssue[];
  lineCount: number;
  issueDensity: number; // issues / 1000 lines
}

/** Full output that can be persisted or displayed */
export interface TypeAnalysisReport {
  generatedAt: string;               // ISO timestamp
  projectRoot: string;
  summary: ReportSummary;
  files: FileReport[];
  recommendations: Recommendation[];
}

/** Actionable advice derived from the aggregated data */
export interface Recommendation {
  id: string;
  priority: number;                  // 1 = highest
  category: IssueCategory;
  title: string;
  description: string;
  estimatedImpact: 'high' | 'medium' | 'low';
  affectedFiles: string[];
  fixSuggestion: string;
}