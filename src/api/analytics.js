import express from 'express';
import { Router } from 'express';
import axios from 'axios';

const router = Router();

router.get('/analytics', async (req, res) => {
  try {
    const response = await axios.get('https://api.example.com/analytics');
    const analyticsData = response.data;
    res.json(analyticsData);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Failed to fetch analytics data' });
  }
});

export default router;