import { Router } from 'express';
import DocsController from '../controllers/docs.controller';

const router = Router();

/**
 * Public endpoint exposing generated workflow documentation.
 *
 * GET /docs/workflow → Markdown document
 */
router.get('/workflow', DocsController.getWorkflowDocs);

export default router;