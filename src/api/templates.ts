import { Router } from 'express';
import fs from 'fs';
import path from 'path';

const router = Router();

router.get('/', (req, res) => {
  const templatesDir = path.join(__dirname, '../../templates/library');
  const templates = fs.readdirSync(templatesDir).map((file) => {
    const filePath = path.join(templatesDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    return {
      name: file.replace('.yaml', ''),
      description: `Template for ${file.replace('.yaml', '')}`,
      content,
    };
  });

  res.json(templates);
});

export default router;