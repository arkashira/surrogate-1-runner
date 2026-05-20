export type Tier = 'free' | 'pro' | 'enterprise';

export interface Dashboard {
  id: string;
  name: string;
  createdAt: Date;
  ownerId: string;
}

export interface Alert {
  id: string;
  name: string;
  condition: AlertCondition;
  dashboardId: string;
  ownerId: string;
  enabled: boolean;
}

export interface AlertCondition {
  metric: 'cost' | 'usage' | 'budget';
  operator: 'gt' | 'lt' | 'eq' | 'gte' | 'lte';
  threshold: number;
}

export interface OpenAPIConfig {
  enabled: boolean;
  apiKey: string;
  baseUrl: string;
  documentationUrl: string;
}

export interface TierLimits {
  maxDashboards: number | 'unlimited';
  maxAlerts: number;
  apiAccess: boolean;
  apiDocumentation: boolean;
}

export const TIER_LIMITS: Record<Tier, TierLimits> = {
  free: {
    maxDashboards: 'unlimited',
    maxAlerts: 5,
    apiAccess: true,
    apiDocumentation: true,
  },
  pro: {
    maxDashboards: 'unlimited',
    maxAlerts: 50,
    apiAccess: true,
    apiDocumentation: true,
  },
  enterprise: {
    maxDashboards: 'unlimited',
    maxAlerts: -1, // unlimited
    apiAccess: true,
    apiDocumentation: true,
  },
};

export class FreeTierService {
  private dashboards: Map<string, Dashboard> = new Map();
  private alerts: Map<string, Alert> = new Map();
  private userTier: Map<string, Tier> = new Map();
  private openApiConfigs: Map<string, OpenAPIConfig> = new Map();

  constructor() {
    // Initialize with free tier as default
  }

  /**
   * Get tier limits for a user
   */
  getTierLimits(userId: string): TierLimits {
    const tier = this.userTier.get(userId) || 'free';
    return TIER_LIMITS[tier];
  }

  /**
   * Check if user can create another dashboard
   * Free tier: unlimited dashboards
   */
  canCreateDashboard(userId: string): boolean {
    const limits = this.getTierLimits(userId);
    return limits.maxDashboards === 'unlimited' || 
           this.getUserDashboards(userId).length < limits.maxDashboards;
  }

  /**
   * Check if user can create another alert
   * Free tier: max 5 alerts
   */
  canCreateAlert(userId: string): boolean {
    const limits = this.getTierLimits(userId);
    const userAlerts = this.getUserAlerts(userId).length;
    
    if (limits.maxAlerts === -1) return true; // unlimited
    return userAlerts < limits.maxAlerts;
  }

  /**
   * Get remaining alert quota for user
   */
  getRemainingAlertQuota(userId: string): number {
    const limits = this.getTierLimits(userId);
    if (limits.maxAlerts === -1) return -1; // unlimited
    
    const used = this.getUserAlerts(userId).length;
    return Math.max(0, limits.maxAlerts - used);
  }

  /**
   * Create a new dashboard (unlimited for free tier)
   */
  createDashboard(userId: string, name: string): Dashboard {
    if (!this.canCreateDashboard(userId)) {
      throw new Error('Dashboard limit reached for your tier');
    }

    const dashboard: Dashboard = {
      id: `dash_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name,
      createdAt: new Date(),
      ownerId: userId,
    };

    this.dashboards.set(dashboard.id, dashboard);
    return dashboard;
  }

  /**
   * Get all dashboards for a user
   */
  getUserDashboards(userId: string): Dashboard[] {
    return Array.from(this.dashboards.values())
      .filter(d => d.ownerId === userId);
  }

  /**
   * Create a new alert (max 5 for free tier)
   */
  createAlert(
    userId: string, 
    name: string, 
    dashboardId: string, 
    condition: AlertCondition
  ): Alert {
    if (!this.canCreateAlert(userId)) {
      throw new Error(`Alert limit reached. Free tier allows up to ${TIER_LIMITS.free.maxAlerts} alerts.`);
    }

    // Verify dashboard belongs to user
    const dashboard = this.dashboards.get(dashboardId);
    if (!dashboard || dashboard.ownerId !== userId) {
      throw new Error('Dashboard not found or does not belong to user');
    }

    const alert: Alert = {
      id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name,
      condition,
      dashboardId,
      ownerId: userId,
      enabled: true,
    };

    this.alerts.set(alert.id, alert);
    return alert;
  }

  /**
   * Get all alerts for a user
   */
  getUserAlerts(userId: string): Alert[] {
    return Array.from(this.alerts.values())
      .filter(a => a.ownerId === userId);
  }
}