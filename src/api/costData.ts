import { Request, Response } from 'express';
import { getCostData } from '../services/costService';

export const getCostDataHandler = async (req: Request, res: Response) => {
  const { startDate, endDate, serviceType } = req.query;
  const data = await getCostData(startDate as string, endDate as string, serviceType as string);
  res.json(data);
};