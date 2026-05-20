import { TierFeatures } from '../types';

export const TIERS: Record<string, TierFeatures> = {
  free: {
    name: 'Free Tier',
    dashboards: 'unlimited',
    alerts: 5,
    apiAccess: true,
    webInterface: true,
  },
  pro: {
    name: 'Pro Tier',
    dashboards: 'unlimited',
    alerts: 50,
    apiAccess: true,
    webInterface: true,
  },
  enterprise: {
    name: 'Enterprise',
    dashboards: 'unlimited',
    alerts: -1, // unlimited
    apiAccess: true,
    webInterface: true,
  },
};