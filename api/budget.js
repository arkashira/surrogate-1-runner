import express from 'express';
import budgetService from '../services/budgetService';

const router = express.Router();

router.post('/', async (req, res) => {
  try {
    const budget = await budgetService.setBudget(req.body.budget);
    res.status(201).send(budget);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

export default router;