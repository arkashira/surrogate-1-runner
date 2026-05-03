
export type RequestStatus = 'open' | 'in_progress' | 'resolved' | 'closed';

export class InvalidTransitionError extends Error {
  constructor(
    public from: RequestStatus,
    public to: RequestStatus,
    public code = 'INVALID_TRANSITION'
  ) {
    super(`Invalid status transition: ${from} -> ${to}`);
    this.name = 'InvalidTransitionError';
  }
}

const TRANSITIONS: Record<RequestStatus, ReadonlySet<RequestStatus>> = {
  open: new Set(['in_progress', 'closed']),
  in_progress: new Set(['resolved', 'open']),
  resolved: new Set(['closed', 'in_progress']),
  closed: new Set(), // terminal; no outgoing transitions
} as const;

export function validateTransition(from: RequestStatus, to: RequestStatus): void {
  // Idempotent same-state is allowed
  if (from === to) return;

  const allowed = TRANSITIONS[from];
  if (!allowed || !allowed.has(to)) {
    throw new InvalidTransitionError(from, to);
  }
}

export function nextStates(from: RequestStatus): ReadonlyArray<RequestStatus> {
  return Array.from(TRANSITIONS[from] || []);
}

export function isTerminal(status: RequestStatus): boolean {
  return status === 'closed';
}