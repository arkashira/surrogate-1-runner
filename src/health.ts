import { Request, Response, NextFunction } from 'express';

export function healthCheck(req: Request, res: Response, next: NextFunction) {
  res.status(200).json({ status: 'ok', service: 'surrogate-1' });
}