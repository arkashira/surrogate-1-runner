import express from 'express';
import { getParserHealth } from '../services/parserService';

const router = express.Router();

router.get('/health', async (req, res) => {
  try {
    const healthStatus = await getParserHealth();
    res.status(200).json(healthStatus);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve parser health' });
  }
});

export default router;