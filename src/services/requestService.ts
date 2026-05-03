// Example: src/routes/requestRoutes.ts
import express from 'express';
import { RequestService } from '../services/requestService';

const router = express.Router();
const requestService = new RequestService();

router.patch('/requests/:id/status', async (req, res) => {
  try {
    const { status } = req.body;
    const actorId = req.user?.id; // or from auth middleware
    const actorType = 'platform_engineer';

    if (!status) {
      return res.status(400).json({ error: 'status is required' });
    }

    const updated = await requestService.updateRequestStatus(
      req.params.id,
      status,
      actorId,
      actorType
    );

    return res.json(updated);
  } catch (err: any) {
    const status = err.status || 500;
    return res.status(status).json({ error: err.message });
  }
});

export default router;