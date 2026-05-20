import express from 'express';
import forecastService from '../services/forecastService';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const forecast = await forecastService.getForecast();
    res.status(200).send({ forecast });
  } catch (error) {
    res.status(500).send(error.message);
  }
});

export default router;