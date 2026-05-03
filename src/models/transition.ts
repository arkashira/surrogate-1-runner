
export type RequestStatus =
  | 'draft'
  | 'submitted'
  | 'in_review'
  | 'approved'
  | 'rejected'
  | 'closed'
  | 'cancelled';

const VALID_TRANSITIONS: Record<RequestStatus, RequestStatus[]> = {
  draft: ['submitted', 'cancelled'],
  submitted: ['in_review', 'cancelled'],
  in_review: ['approved', 'rejected', 'cancelled'],
  approved: ['closed'],
  rejected: ['closed', 'cancelled'],
  closed: [],
  cancelled: [],
};

export const TERMINAL_STATUSES: Set<RequestStatus> = new Set(['closed', 'cancelled']);

export interface Transition {
  requestId: string;
  fromStatus: RequestStatus | null;
  toStatus: RequestStatus;
  actor: string; // user ID or email
  comment: string;
  timestamp: Date;
}

export function isValidTransition(from: RequestStatus | null, to: RequestStatus): boolean {
  if (from === null) {
    // allow initial creation only into non-terminal states
    return !TERMINAL_STATUSES.has(to) && VALID_TRANSITIONS[to] !== undefined;
  }
  return VALID_TRANSITIONS[from]?.includes(to) === true;
}

export function isTerminal(status: RequestStatus): boolean {
  return TERMINAL_STATUSES.has(status);
}

/**
 * Validate and normalize a transition.
 * Throws Error with message suitable for 400 responses.
 */
export function validateTransition(
  from: RequestStatus | null,
  to: RequestStatus,
  actor: string,
  comment: string
): Transition {
  if (!actor || actor.trim().length === 0) {
    throw new Error('Actor is required');
  }

  if (!comment || comment.trim().length === 0) {
    throw new Error('Comment is required');
  }

  if (!Object.keys(VALID_TRANSITIONS).includes(to)) {
    throw new Error(`Invalid status: ${to}`);
  }

  if (from && !Object.keys(VALID_TRANSITIONS).includes(from)) {
    throw new Error(`Invalid current status: ${from}`);
  }

  // Block terminal -> non-terminal
  if (from && TERMINAL_STATUSES.has(from) && !TERMINAL_STATUSES.has(to)) {
    throw new Error('Cannot transition from a terminal status to a non-terminal status');
  }

  if (!isValidTransition(from, to)) {
    const allowed = from ? VALID_TRANSITIONS[from].join(', ') : '(initial non-terminal statuses)';
    throw new Error(`Invalid transition from ${from ?? 'null'} to ${to}. Allowed: ${allowed}`);
  }

  return {
    requestId: '', // caller should populate
    fromStatus: from,
    toStatus: to,
    actor: actor.trim(),
    comment: comment.trim(),
    timestamp: new Date(),
  };
}