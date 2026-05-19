/**
 * Rule Registry - Maps rule IDs to their implementation functions
 */

import { Rule, RuleViolation, LintContext, RuleSeverity } from './types';

// Registry of rule check implementations
const ruleImplementations: Map<string, (context: LintContext) => RuleViolation[]> = new Map();

// Default message generators
const ruleMessages: Map<string, (violation: RuleViolation) => string> = new Map();

/**
 * Register a rule implementation
 */
export function registerRule(
  id: string,
  checkFn: (context: LintContext) => RuleViolation[],
  messageFn?: (violation: RuleViolation) => string
): void {
  ruleImplementations.set(id, checkFn);
  if (messageFn) {
    ruleMessages.set(id, messageFn);
  }
}

/**
 * Get the check function for a rule
 */
export function getRuleCheck(id: string): (context: LintContext) => RuleViolation[] {
  return ruleImplementations.get(id) || (() => []);
}

/**
 * Get the message generator for a rule
 */
export function getRuleMessage(id: string): (violation: RuleViolation) => string {
  return ruleMessages.get(id) || ((v) => `Rule ${v.ruleId} violated`);
}

/**
 * Check if a rule has an implementation
 */
export function hasRuleImplementation(id: string): boolean {
  return ruleImplementations.has(id);
}

/**
 * Register all built-in rules
 */
export function registerBuiltinRules(): void {
  // no-debugger rule
  registerRule('no-debugger', (context) => {
    const violations: RuleViolation[] = [];
    if (!context.fileContent) return violations;
    
    const lines = context.fileContent.split('\n');
    lines.forEach((line, index) => {
      if (line.includes('debugger')) {
        violations.push({
          ruleId: 'no-debugger',
          message: 'Unexpected debugger statement',
          severity: RuleSeverity.Error,
          file: context.filePath,
          line: index + 1
        });
      }
    });
    return violations;
  });

  // no-console rule
  registerRule('no-console', (context) => {
    const violations: RuleViolation[] = [];
    if (!context.fileContent) return violations;
    
    const lines = context.fileContent.split('\n');
    lines.forEach((line, index) => {
      if (line.match(/\bconsole\.(log|warn|error|info)\(/)) {
        violations.push({
          ruleId: 'no-console',
          message: 'Console statement found',
          severity: RuleSeverity.Warning,
          file: context.filePath,
          line: index + 1
        });
      }
    });
    return violations;
  });

  // require-types rule
  registerRule('require-types', (context) => {
    const violations: RuleViolation[] = [];
    // Simplified check - in production would use AST
    if (!context.fileContent) return violations;
    
    const lines = context.fileContent.split('\n');
    lines.forEach((line, index) => {
      // Detect functions without type annotations
      if (line.match(/function\s+\w+\s*\([^)]*\)\s*{/) && !line.includes(':')) {
        violations.push({
          ruleId: 'require-types',
          message: 'Missing type annotation',
          severity: RuleSeverity.Warning,
          file: context.filePath,
          line: index + 1
        });
      }
    });
    return violations;
  });
}