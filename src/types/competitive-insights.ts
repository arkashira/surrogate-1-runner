export interface CompetitiveInsight {
  id: string;
  title: string;
  description: string;
  category: 'pricing' | 'product' | 'market' | 'strategy';
  severity: 'critical' | 'warning' | 'info' | 'success';
  actionable: boolean;
  createdAt: string;
}

export interface MarketTrend {
  date: string;
  value: number;
  change: number;
}

export interface PricePoint {
  competitorId: string;
  competitorName: string;
  price: number;
  vsUs: number; // percentage difference
  trend: 'up' | 'down' | 'stable';
  rating: number; // 1-5
}

export interface CompetitorData {
  id: string;
  name: string;
  category: string;
  currentPrice: number;
  marketShare: number;
  pricePosition: 'premium' | 'mid' | 'budget';
  trend: 'up' | 'down' | 'stable';
  priceChange: number;
}

export interface CompetitiveInsightsData {
  insights: CompetitiveInsight[];
  trends: MarketTrend[];
  competitors: CompetitorData[];
  pricePoints: PricePoint[];
  lastUpdated: string;
}