// /opt/axentx/surrogate-1/src/routes/public/requests.ts
import { Router, Request, Response, NextFunction } from 'express';
import { serializePublicRequest, PublicRequest } from '../../serializers/publicRequestSerializer';

// Replace with real repository/DB call and soft-delete check.
// Return null for non-existent or deleted requests to trigger 404.
async function findPublicRequestById(id: string): Promise<PublicRequest | null> {
  // Example stub:
  const demo: Record<string, PublicRequest> = {
    'req-123': {
      id: 'req-123',
      title: 'Dataset export #42',
      status: 'processing',
      isDeleted: false,
      sla: {
        targetHours: 72,
        dueAt: new Date(Date.now() + 72 * 3600_000).toISOString(),
        status: 'on_track',
      },
      updatedAt: new Date().toISOString(),
      timeline: [
        { timestamp: new Date(Date.now() - 3600_000).toISOString(), status: 'created', message: 'Request submitted' },
        { timestamp: new Date().toISOString(), status: 'processing', message: 'Ingest started' },
      ],
    },
  };
  const found = demo[id] || null;
  if (!found || found.isDeleted) return null;
  return found;
}

const router = Router();

/**
 * GET /public/requests/:id
 * Public status endpoint (no auth required).
 * - Returns 404 for non-existent or deleted requests.
 * - Permits embedding via iframe (headers below).
 */
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    if (!id || typeof id !== 'string' || id.trim() === '') {
      return res.status(404).send();
    }

    const request = await findPublicRequestById(id);
    if (!request) {
      return res.status(404).send();
    }

    // Iframe-embeddable and public caching.
    // Use SAMEORIGIN by defau
