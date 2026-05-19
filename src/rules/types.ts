/**
 * Rule types and interfaces
 */

export enum RuleSeverity {
  Error = 'error',
  Warning = 'warning',
  Info = 'info'
}

export interface RuleViolation {
  ruleId: string;
  message: string;
  severity: RuleSeverity;
  line?: number;
  column?: number;
  file?: string;
}

export interface RuleDefinition {
  id: string;
  name: string;
  description: string;
  severity?: RuleSeverity;
  enabled?: boolean;
}

export interface Rule extends RuleDefinition {
  severity: RuleSeverity;
  enabled: boolean;
  check: (context: LintContext) => RuleViolation[];
  message: (violation: RuleViolation) => string;
}

export interface LintContext {
  repoPath: string;
  filePath?: string;
  fileContent?: string;
  ast?: any;
}

/**
 * Format a rule violation as a comment
 */
export function formatViolationAsComment(violation: RuleViolation): string {
  const severity = violation.severity.toUpperCase();
  const location = violation.file 
    ? `${violation.file}${violation.line ? `:${violation.line}` : ''}`
    : 'unknown';
  
  return `[${severity}] ${violation.ruleId}: ${violation.message} (${location})`;
}