import express, { Request, Response } from 'express';
import { updateTrainingDataset, getCommunityValidationStats } from '../services/outcome-service';

const router = express.Router();

interface OutcomeReport {
  userId: string;
  outcomeType: 'success' | 'pivot' | 'failure';
  feedback?: string;
}

router.post('/report', async (req: Request, res: Response) => {
  try {
    const outcomeReport: OutcomeReport = req.body;
    await updateTrainingDataset(outcomeReport);
    const stats = await getCommunityValidationStats();
    res.status(200).json({ message: 'Outcome reported successfully', stats });
  } catch (error) {
    res.status(500).json({ message: 'Failed to report outcome', error: error.message });
  }
});

export default router;