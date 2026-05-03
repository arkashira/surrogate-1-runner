import express, { Request, Response, NextFunction } from 'express';
import fs from 'fs';
import { getDocumentFile } from '../services/storage';

const router = express.Router();

/**
 * GET /documents/:id/file
 * Streams a document file with Range request support.
 */
router.get('/:id/file', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const doc = getDocumentFile(req.params.id);
    if (!doc) {
      return res.status(404).json({ error: 'Document not found' });
    }

    const { size } = doc;
    const range = req.headers.range;

    res.setHeader('Accept-Ranges', 'bytes');

    if (!range) {
      res.setHeader('Content-Type', doc.mime);
      res.setHeader('Content-Length', String(size));
      const stream = fs.createReadStream(doc.path);
      stream.on('error', () =>
