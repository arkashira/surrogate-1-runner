import { Router, Request, Response } from 'express';
import * as shellService from '../services/shellService';

const router = Router();

/**
 * GET /sessions
 * Returns a list of active shell sessions.
 */
router.get('/sessions', async (req: Request, res: Response) => {
  try {
    const sessions = await shellService.getActiveSessions();
    res.json(sessions);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/**
 * POST /sessions/:id/terminate
 * Terminates an active shell session.
 */
router.post('/sessions/:id/terminate', async (req: Request, res: Response) => {
  const sessionId = req.params.id;
  try {
    await shellService.terminateSession(sessionId);
    res.status(200).json({ success: true, sessionId });
  } catch (err) {
    const error = err as Error;
    // If the session was not found, return 404
    if (error.message === 'SessionNotFound') {
      res.status(404).json({ error: 'Session not found' });
    } else {
      res.status(500).json({ error: error.message });
    }
  }
});

export default router;