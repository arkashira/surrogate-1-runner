
import { validateTransition, InvalidTransitionError, RequestStatus } from '../lib/requestStateMachine';

export type AuditEntry = {
  timestamp: string; // ISO
  previousStatus: RequestStatus;
  newStatus: RequestStatus;
  changedBy?: string;
  reason?: string;
};

export type Request = {
  id: string;
  title: string;
  status: RequestStatus;
  auditLog: AuditEntry[];
  updatedAt: string;
};

// In-memory store for demo; replace with DB/ORM in production.
const requests = new Map<string, Request>();

export async function patchRequestStatus(
  id: string,
  nextStatus: RequestStatus,
  changedBy?: string,
  reason?: string
): Promise<Request> {
  const req = requests.get(id);
  if (!req) {
    const err: any = new Error('Request not found');
    err.status = 404;
    throw err;
  }

  const previousStatus = req.status;

  // Validate transition (throws InvalidTransitionError on invalid)
  validateTransition(previousStatus, nextStatus);

  const now = new Date().toISOString();
  const auditEntry: AuditEntry = {
    timestamp: now,
    previousStatus,
    newStatus: nextStatus,
    changedBy,
    reason,
  };

  const updated: Request = {
    ...req,
    status: nextStatus,
    auditLog: [...req.auditLog, auditEntry],
    updatedAt: now,
  };

  requests.set(id, updated);
  return updated;
}

// Framework-agnostic HTTP adapter for PATCH /requests/:id/status
export async function handlePatchRequestStatus(req: {
  params: { id: string };
  body: { status: RequestStatus; changedBy?: string; reason?: string };
}) {
  try {
    const updated = await patchRequestStatus(req.params.id, req.body.status, req.body.changedBy, req.body.reason);
    return { status: 200, body: updated };
  } catch (err: any) {
    if (err instanceof InvalidTransitionError) {
      return {
        status: 400,
        body: { error: err.message, code: err.code },
      };
    }
    return {
      status: err.status || 500,
      body: { error: err.message, code: err.code },
    };
  }
}