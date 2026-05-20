import { Router } from 'express';
import { confirmPasswordReset } from './passwordResetConfirmation';

const router = Router();

router.post('/password-reset/confirm', confirmPasswordReset);

export default router;