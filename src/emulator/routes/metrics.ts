import express, { Request, Response } from 'express';
import { createRateLimiter } from '../middleware/rateLimit';

const router = express.Router();
// 1200 requests per hour (1 request per second)
const limiter = createRateLimiter(1200, 3600000);

router.post('/api/v1/series', limiter, (req: Request, res: Response) => {
  // Validate request body structure
  if (!req.body || !Array.isArray(req.body.series)) {
    return res.status(400).json({
      errors: [
        {
          message: 'Invalid payload format: "series" array is required',
        }
      ]
    });
  }

  // Simulate successful processing
  res.status(202).json({
    status: 'ok',
    processed: req.body.series.length
  });
});

export default router;