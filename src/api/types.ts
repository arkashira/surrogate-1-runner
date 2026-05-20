export interface DashboardFeature {
  unlimited: boolean;
  limit: number | null; // null = unlimited
}

export interface AlertFeature {
  limit: number;          // 5 for free, 50 for pro, -1 for unlimited
  current: number;        // how many the user has already created
}

export interface AccessFeature {
  api: boolean;
  webInterface: boolean;
}

export interface FreeTierFeatures {
  dashboards: DashboardFeature;
  alerts: AlertFeature;
  access: AccessFeature;
  tier: 'free' | 'pro' | 'enterprise';
}