import express from 'express';
import policyService from './policy-service';

const router = express.Router();

router.post('/', async (req, res) => {
  try {
    const policy = req.body;
    const createdPolicy = await policyService.createPolicy(policy);
    res.json(createdPolicy);
  } catch (error) {
    res.status(500).json({ message: 'Failed to create policy' });
  }
});

export default router;