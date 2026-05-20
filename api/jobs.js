
import express from 'express';
import axios from 'axios';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:3001/api/jobs');
    res.json(response.data);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

export default router;