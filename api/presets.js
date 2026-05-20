
import express from 'express';
import axios from 'axios';

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:3000/api/presets');
    res.json(response.data);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

export default router;