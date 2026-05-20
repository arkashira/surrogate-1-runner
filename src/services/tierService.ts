import { FreeTierFeatures } from '../api/types';

const tiers: Record<string, FreeTierFeatures> = {
  free: {
    dashboards: { unlimited: true, limit: null },
    alerts: { limit: 5, current: 0 },
    access: { api: true, webInterface: true },
    tier: 'free',
  },
  pro: {
    dashboards: { unlimited: true, limit: null },
    alerts: { limit: 50, current: 0 },
    access: { api: true, webInterface: true },
    tier: 'pro',
  },
  enterprise: {
    dashboards: { unlimited: true, limit: null },
    alerts: { limit: -1, current: 0 }, // -1 = unlimited
    access: { api: true, webInterface: true },
    tier: 'enterprise',
  },
};

/**
 * Return the feature set for a given tier.
 * @param tierName 'free' | 'pro' | 'enterprise'
 */
export function getTierFeatures(tierName: string = 'free'): FreeTierFeatures {
  return tiers[tierName] ?? tiers.free;
}