import { Router, Request, Response } from 'express';
import fs from 'fs';
import path from 'path';

const router = Router();

const DATA_FILE = path.resolve(process.cwd(), '.axentx-requests.json');

type RequestStatus = 'submitted' | 'in_progress' | 'blocked' | 'done';

interface StoredRequest {
  id: string;
  status: RequestStatus;
  createdAt: string; // ISO
  updatedAt: string; // ISO
  slaTargetMinutes?: number;
  previousStatus?: RequestStatus;
}

interface UpdateStatusBody {
  status: RequestStatus;
  slaTargetMinutes?: number;
}

function loadRequests(): Record<string, StoredRequest> {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf8');
      const parsed = JSON.parse(raw || '{}');
      // Basic shape validation
      if (parsed && typeof parsed === 'object') return parsed as Record<string, StoredRequest>;
    }
  } catch {
    // ignore corruption; start fresh
  }
  return {};
}

function saveRequests(requests: Record<string, StoredRequest>): void {
  try {
    fs.mkdirSync(path.dirname(DATA_FILE), { recursive: true });
    fs.writeFileSync(DATA_FILE, JSON.stringify(requests, null, 2), 'utf8');
  } catch {
    // best-effort persistence; caller can decide to warn/retry
  }
}

const ALLOWED_TRANSITIONS: Record<RequestStatus, RequestStatus[]> = {
  submitted: ['in_progress', 'blocked'],
  in_progress: ['blocked', 'done'],
  blocked: ['in_progress', 'done'],
  done: [] // terminal
};

function computeSlaElapsedMinutes(createdAt: string): number {
  const start = new Date(createdAt).getTime();
  if (isNaN(start)) return 0;
  return Math.max(0, Math.floor((Date.now() - start) / 60000));
}

function isSlaBreached(req: StoredRequest): boolean {
  if (!req.slaTargetMinutes || req.slaTargetMinutes <= 0) return false;
  return computeSlaElapsedMinutes(req.createdAt) > req.slaTargetMinutes;
}

function buildResponse(req: StoredRequest) {
  const slaElapsed = computeSlaElapsedMinutes(req.createdAt);
  const breached = isSlaBreached(req);
  return {
    id: req.id,
    status: req.status,
    previousStatus: req.previousStatus,
    createdAt: req.createdAt,
    updatedAt: req.updatedAt,
    slaElapsedMinutes: slaElapsed,
    slaTargetMinutes: req.slaTargetMinutes,
    slaBreached: breached,
    allowedTransitions: ALLOWED_TRANSITIONS[req.status]
  };
}

/**
 * PUT /requests/:id/status
 * Body: { status: RequestStatus, slaTargetMinutes?: number }
 */
router.put('/:id/status', (req: Request<{ id: string }, any, UpdateStatusBody>, res: Response) => {
  const id = req.params.id;
  const { status, slaTargetMinutes } = req.body || {};

  if (!status || !['submitted', 'in_progress', 'blocked', 'done'].includes(status)) {
    return res.status(400).json({ error: 'Invalid status value' });
  }

  const requests = loadRequests();
  let stored = requests[id];

  // Create on first touch with submitted as initial state
  if (!stored) {
    const now = new Date().toISOString();
    stored = { id, status: 'submitted', createdAt: now, updatedAt: now };
    requests[id] = stored;
  }

  // Apply SLA target if provided
  if (slaTargetMinutes !== undefined) {
    stored.slaTargetMinutes = slaTargetMinutes;
  }

  // Terminal reject
  if (stored.status === 'done') {
    return res.status(400).json({ error: 'Cannot transition from done', allowed: [] });
  }

  // Validate transition
  const allowed = ALLOWED_TRANSITIONS[stored.status];
  if (!allowed.includes(status)) {
    return res.status(400).json({
      error: `Invalid transition from ${stored.status} to ${status}`,
      allowed
    });
  }

  // Apply intended transition
  stored.previousStatus = stored.status;
  stored.status = status;
  stored.updatedAt = new Date().toISOString();

  // SLA breach reflection: if breached, force blocked and preserve intent
  if (isSlaBreached(stored)) {
    if (stored.status !== 'blocked') {
      stored.previousStatus = stored.status;
      stored.status = 'blocked';
    }
    stored.updatedAt = new Date().toISOString();
  }

  saveRequests(requests);
  return res.json(buildResponse(stored));
});

/**
 * GET /requests/:id
 */
router.get('/:id', (req, res) => {
  const id = req.params.id;
  const requests = loadRequests();
  const stored = requests[id];
  if (!stored) return res.status(404).json({ error: 'Request not found' });
  return res.json(buildResponse(stored));
});

export default router;