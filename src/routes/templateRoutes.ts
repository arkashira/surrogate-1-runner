import { Router } from 'express';
import {
  createTemplate,
  getTemplate,
  listTemplates,
  updateTemplate,
  deleteTemplate,
} from '../controllers/TemplateController';

const router = Router();

router.post('/', createTemplate);
router.get('/', listTemplates);
router.get('/:id', getTemplate);
router.put('/:id', updateTemplate);
router.delete('/:id', deleteTemplate);

export default router;