{
  "need_clarification": true,
  "reason": "Project mismatch: surrogate-1 is a data pipeline runner (README describes 'parallel public-dataset ingest workers'), but task requests a React hook for radio recording UI. No hooks directory or frontend code visible in project context.",
  "request_to": "architect-daemon",
  "minimal_spec_needed": "Confirm project structure: is there a separate frontend repo, or should recording logic be implemented in the surrogate-1 runner's existing codebase? What tech stack (React/Vue/etc) and file locations should I use for the recording hook?"
}