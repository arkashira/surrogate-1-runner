import express from 'express';
import pdfExportRouter from './pdfExport';

const router = express.Router();

router.use('/pdf', pdfExportRouter);

export default router;