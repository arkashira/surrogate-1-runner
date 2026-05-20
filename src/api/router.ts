import { Router } from 'express';
import { freeTierHandler, tierFeaturesHandler } from './controller';

const router = Router();

/**
 * GET /api/v1/tier/free
 * Retrieve free‑tier features
 */
router.get('/free', freeTierHandler);

/**
 * GET /api/v1/tier/features?tier=free|pro|enterprise
 * Retrieve features for the requested tier
 */
router.get('/features', tierFeaturesHandler);

export default router;