import { Router } from 'express';
import deleteSandboxApi from '../sandboxes/delete';

const router = Router();

router.delete('/:sandboxId', deleteSandboxApi);

export default router;