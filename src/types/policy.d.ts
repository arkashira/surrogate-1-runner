/**
 * Core type definitions for cost policies.
 *
 * A policy is a collection of rules that are evaluated against a
 * provisioning request (the "resource").  Each rule has a concrete
 * `type` that determines which validator should be applied.
 *
 * The engine (src/core/policy-engine.ts) knows how to interpret the
 * rule types defined here.
 */

export type PolicyId = string;

/**
 * Top‑level policy object.
 */
export interface Policy {
  /** Unique identifier for the policy. */
  id: PolicyId;
  /** Human‑readable name. */
  name: string;
  /** Optional description. */
  description?: string;
  /** If true, the engine will attempt auto‑remediation on violations. */
  autoRemediate?: boolean;
  /** Rules that belong to this policy. */
  rules: PolicyRule[];
}

/**
 * Union of all supported rule definitions.
 */
export type PolicyRule = MaxInstanceSizeRule | IdleTimeoutRule;

/**
 * Rule that caps the allowed instance size.
 *
 * Example:
 *   { type: 'maxInstanceSize', maxSize: 'm5.large' }
 */
export interface MaxInstanceSizeRule {
  /** Discriminator for the rule type. */
  type: 'maxInstanceSize';
  /** The maximum allowed instance size (cloud‑provider specific string). */
  maxSize: string;
}

/**
 * Rule that caps the allowed idle timeout (in seconds).
 *
 * Example:
 *   { type: 'idleTimeout', maxSeconds: 300 }
 */
export interface IdleTimeoutRule {
  type: 'idleTimeout';
  /** Maximum idle timeout in seconds. */
  maxSeconds: number;
}

/**
 * Result of a single rule evaluation.
 */
export interface RuleViolation {
  /** The policy that generated this violation. */
  policyId: PolicyId;
  /** The rule that was violated. */
  rule: PolicyRule;
  /** Human‑readable message describing the problem. */
  message: string;
}

/**
 * Result of validating a resource against a set of policies.
 */
export interface ValidationResult {
  /** All rule violations found (empty if none). */
  violations: RuleViolation[];
  /** Whether any violations were found. */
  hasViolations: boolean;
}