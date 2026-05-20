import express, { Request, Response } from 'express';
import path from 'path';
import { promises as fs } from 'fs';
import { OptimizationSuggestion } from './types';

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

// In‑memory store for acknowledgements (replace with DB in prod)
const acknowledged = new Set<string>();

// Middleware
app.use(express.json());

// Serve the static React bundle
app.use('/static', express.static(path.join(__dirname, '..', 'public')));

// Serve the HTML page
app.get('/', (_req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, 'web-interface.html'));
});

/**
 * API: GET /api/suggestions
 * Returns a list of actionable optimization suggestions.
 */
app.get('/api/suggestions', async (_req: Request, res: Response) => {
  try {
    const suggestions: OptimizationSuggestion[] = [
      {
        id: 's1',
        title: 'Resize under‑utilized EC2 instances',
        description:
          'Instance type t3.micro is running at <10% CPU for the last 24h. Consider switching to t3.small to reduce cost.',
        action: 'Update instance type in your cloud console',
      },
      {
        id: 's2',
        title: 'Enable S3 Intelligent‑Tiering',
        description:
          'Your S3 bucket has infrequently accessed objects. Switching to Intelligent‑Tiering can reduce storage costs by up to 30%.',
        action: 'Enable Intelligent‑Tiering via the S3 console',
      },
    ];

    // Mark already acknowledged suggestions
    const enriched = suggestions.map(s => ({
      ...s,
      acknowledged: acknowledged.has(s.id),
    }));

    res.json({ suggestions: enriched });
  } catch (err) {
    console.error('Error fetching suggestions:', err);
    res.status(500).json({ error: 'Failed to retrieve suggestions' });
  }
});

/**
 * API: POST /api/suggestions/:id/ack
 * Marks a suggestion as implemented.
 */
app.post('/api/suggestions/:id/ack', async (req: Request, res: Response) => {
  const { id } = req.params;
  acknowledged.add(id);
  console.log(`Suggestion ${id} acknowledged by user`);
  res.json({ status: 'acknowledged', id });
});

app.listen(PORT, () => {
  console.log(`Surrogate‑1 web interface listening on port ${PORT}`);
});

export default app;