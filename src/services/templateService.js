
import axios from 'axios';

export function useTemplate(id) {
  const [template, setTemplate] = React.useState(null);

  React.useEffect(() => {
    axios.get(`/api/templates/${id}`)
      .then(res => setTemplate(res.data))
      .catch(err => console.error(err));
  }, [id]);

  return template;
}

// src/services/templateApi.js

import axios from 'axios';

export const API_URL = '/api';

export function getTemplate(id) {
  return axios.get(`${API_URL}/templates/${id}`);
}

// src/api/templates.js

import express from 'express';
import { Router } from 'express';
import getTemplate from '../services/templateApi';

const router = Router();

router.get('/:id', async (req, res) => {
  try {
    const template = await getTemplate(req.params.id);
    res.json(template);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

export default router;