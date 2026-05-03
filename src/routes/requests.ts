import { Router } from 'express';
import { db } from '../db';
import { computeSlaStatus, VALID_TRANSITIONS } from '../lib/sla';

const router = Router();

// PATCH /requests/:id/state
router.patch('/:id/state', (req, res) => {
  const { id } = req.params;
  const { state, changed_by, reas
