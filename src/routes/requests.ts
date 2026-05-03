import { Router, Request, Response } from 'express';
import { generatePublicUrl } from '../lib/url';

const router = Router();

// In-memory store for example; replace with DB in production
const requests: Array<{
  id: string;
  title: string;
  type: string;
  owner: string;
  slaTarget?: string | null;
  status: 'open' | 'in_progress' | 'closed';
  createdAt: string;
  updatedAt: string;
  publicUrl: string;
}> = [];

function isValidISODurationOrDate(value: string): boolean {
  // Accept either ISO 8601 duration (PnYnMnDTnHnMnS) or date string
  const isoDuration = /^P(?:\d+Y)?(?:\n?\d+M)?(?:\n?\d+W)?(?:\n?\d+D)?(?:T(?:\n?\d+H)?(?:\n?\d+M)?(?:\n?\d+S)?)?$/;
  if (isoDuration.test(value)) return true;
  // Valid date string that Date can parse and is not NaN
  const d = new Date(value);
  return !isNaN(d.getTime());
}

// POST /requests
router.post('/', (req: Request, res: Response) => {
  const { title, type, owner, slaTarget } = req.body;

  if (!title || typeof title !== 'string' || title.trim() === '') {
    return res.status(400).json({ error: 'Missing or invalid title' });
  }
  if (!type || typeof type !== 'string' || type.trim() === '') {
    return res.status(400).json({ error: 'Missing or invalid type' });
  }
  if (!owner || typeof owner !== 'string' || owner.trim() === '') {
    return res.status(400).json({ error: 'Missing or invalid owner' });
  }
  if (slaTarget !== undefined && slaTarget !== null && !isValidISODurationOrDate(String(slaTarget))) {
    return res.status(400).json({ error: 'Invalid SLA target' });
  }

  const id = `req_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
  const now = new Date().toISOString();
  const publicUrl = generatePublicUrl(title, type, owner, slaTarget);

  const newRequest = {
    id,
    title: title.trim(),
    type: type.trim(),
    owner: owner.trim(),
    slaTarget: slaTarget ? String(slaTarget).trim() : null,
    status: 'open' as const,
    createdAt: now,
    updatedAt: now,
    publicUrl,
  };

  requests.push(newRequest);

  return res.status(201).json({
    id: newRequest.id,
    publicUrl: newRequest.publicUrl,
    status: newRequest.status,
  });
});

// GET /requests
router.get('/', (_req: Request, res: Response) => {
  return res.json(
    requests.map((r) => ({
      id: r.id,
      title: r.title,
      type: r.type,
      owner: r.owner,
      slaTarget: r.slaTarget,
      status: r.status,
      createdAt: r.createdAt,
      updatedAt: r.updatedAt,
      publicUrl: r.publicUrl,
    }))
  );
});

export default router;