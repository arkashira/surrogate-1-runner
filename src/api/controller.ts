import { Request, Response, NextFunction } from 'express';
import { getTierFeatures } from '../services/tierService';
import { FreeTierFeatures } from './types';

export function freeTierHandler(req: Request, res: Response, next: NextFunction) {
  try {
    const features = getTierFeatures('free');
    res.status(200).json({
      success: true,
      data: features,
      message: 'Free‑tier features retrieved successfully',
    });
  } catch (err) {
    next(err);
  }
}

export function tierFeaturesHandler(req: Request, res: Response, next: NextFunction) {
  try {
    const tier = (req.query.tier as string) ?? 'free';
    const features = getTierFeatures(tier);
    res.status(200).json({
      success: true,
      data: features,
      message: `${features.tier} tier features retrieved successfully`,
    });
  } catch (err) {
    next(err);
  }
}