/**
 * Surrogate-1 Cloud Cost Transparency - Tier Service
 * 
 * Acceptance Criteria:
 * - Free-tier includes unlimited dashboards
 * - Free-tier includes up to 5 alerts
 * - Free-tier is accessible via API and web interface
 */

export type TierType = 'free' | 'pro' | 'enterprise';

export interface TierLimits {
  maxDashboards: number | 'unlimited';
  maxAlerts: number | 'unlimited';
  apiAccess: boolean;
  webInterface: boolean;
  supportLevel: 'email' | 'priority' | 'dedicated';
}

export interface UserTier {
  tier: TierType;
  dashboardCount: number;
  alertCount: number;
  features: TierLimits;
  updatedAt: Date;
}

// Explicit unlimited sentinel (clearer than -1)
export const UNLIMITED = 'unlimited' as const;

export const TIER_CONFIGS: Record<TierType, TierLimits> = {
  free: {
    maxDashboards: UNLIMITED,
    maxAlerts: 5,
    apiAccess: true,
    webInterface: true,
    supportLevel: 'email',
  },
  pro: {
    maxDashboards: UNLIMITED,
    maxAlerts: 50,
    apiAccess: true,
    webInterface: true,
    supportLevel: 'priority',
  },
  enterprise: {
    maxDashboards: UNLIMITED,
    maxAlerts: UNLIMITED,
    apiAccess: true,
    webInterface: true,
    supportLevel: 'dedicated',
  },
};

const TIER_NAMES: Record<TierType, string> = {
  free: 'Free',
  pro: 'Pro',
  enterprise: 'Enterprise',
};

/**
 * Get user's current tier with usage counts
 * In production, this fetches from database
 */
export async function getUserTier(userId: string): Promise<UserTier> {
  if (!userId || typeof userId !== 'string') {
    throw new Error('Invalid userId provided');
  }
  
  // TODO: Replace with actual database query
  // const user = await db.users.findUnique({ where: { id: userId }};
  const tier = 'free' as TierType;
  const features = TIER_CONFIGS[tier];
  
  return {
    tier,
    dashboardCount: 0,
    alertCount: 0,
    features,
    updatedAt: new Date(),
  };
}

/**
 * Check if user can create another dashboard
 */
export function canCreateDashboard(user: UserTier): boolean {
  const { maxDashboards } = user.features;
  
  if (maxDashboards === UNLIMITED) {
    return true;
  }
  
  return user.dashboardCount < maxDashboards;
}

/**
 * Check if user can create another alert
 */
export function canCreateAlert(user: UserTier): boolean {
  const { maxAlerts } = user.features;
  
  if (maxAlerts === UNLIMITED) {
    return true;
  }
  
  return user.alertCount < maxAlerts;
}

/**
 * Get remaining alerts user can create
 */
export function getRemainingAlerts(user: UserTier): number {
  const { maxAlerts } = user.features;
  
  if (maxAlerts === UNLIMITED) {
    return Infinity;
  }
  
  return Math.max(0, maxAlerts - user.alertCount);
}

/**
 * Get formatted tier information for API response
 */
export function getTierInfo(userId: string): Promise<{
  tier: TierType;
  tierName: string;
  limits: TierLimits;
  usage: {
    dashboards: number;
    alerts: number;
  };
  canAccessApi: boolean;
  canAccessWeb: boolean;
}> {
  return getUserTier(userId).then(user => ({
    tier: user.tier,
    tierName: TIER_NAMES[user.tier],
    limits: user.features,
    usage: {
      dashboards: user.dashboardCount,
      alerts: user.alertCount,
    },
    canAccessApi: user.features.apiAccess,
    canAccessWeb: user.features.webInterface,
  }));
}

/**
 * Validate dashboard creation request
 */
export function validateDashboardCreation(
  user: UserTier
): { valid: boolean; reason?: string } {
  if (!canCreateDashboard(user)) {
    const limit = user.features.maxDashboards;
    return {
      valid: false,
      reason: `Dashboard limit reached (${limit} dashboards)`,
    };
  }
  return { valid: true };
}

/**
 * Validate alert creation request
 */
export function validateAlertCreation(
  user: UserTier
): { valid: boolean; reason?: string; remaining?: number } {
  if (!canCreateAlert(user)) {
    return {
      valid: false,
      reason: `Alert limit reached (${user.features.maxAlerts} alerts on ${user.tier} tier)`,
      remaining: 0,
    };
  }
  
  const remaining = getRemainingAlerts(user);
  return { valid: true, remaining };
}