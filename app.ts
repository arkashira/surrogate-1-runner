import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import swaggerUi from 'swagger-ui-express';
import { openApiDocument } from './api/openapi';
import { errorHandler } from './api/middleware/errorHandler';
import { authMiddleware } from './api/middleware/auth';
import { rateLimiter } from './api/middleware/rateLimit';
import dashboardRoutes from './api/routes/dashboards';
import costRoutes from './api/routes/costs';
import alertRoutes from './api/routes/alerts';
import { logger } from './utils/logger';

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(rateLimiter);
app.use(authMiddleware); // API‑Key auth

// Swagger UI
app.use('/docs', swaggerUi.serve, swaggerUi.setup(openApiDocument));

// API routes
app.use('/api/v1/dashboards', dashboardRoutes);
app.use('/api/v1/dashboards', costRoutes);   // nested under dashboards
app.use('/api/v1/alerts', alertRoutes);

// Global error handler
app.use(errorHandler);

export default app;