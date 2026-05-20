import express, { Express, Request, Response, NextFunction } from 'express';
import tierRoutes from './api/router';
import { healthCheck } from './health';

const app: Express = express();
const PORT = process.env.PORT ?? 3000;

// Middleware
app.use(express.json());

// Health‑check
app.get('/health', healthCheck);

// API routes
app.use('/api/v1/tier', tierRoutes);

// Root endpoint – useful for quick sanity checks
app.get('/', (_req: Request, res: Response) => {
  res.status(200).json({
    name: 'Surrogate‑1 Cloud Cost Transparency API',
    version: '1.0.0',
    endpoints: {
      freeTier: '/api/v1/tier/free',
      tierFeatures: '/api/v1/tier/features',
    },
  });
});

// Global error handler – keeps controller code clean
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error(err);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
  console.log(`Surrogate‑1 API running on port ${PORT}`);
});

export default app; // exported for testing