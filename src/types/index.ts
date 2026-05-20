export interface PricingData {
  price: number;
  currency: string;
  source: string;
  timestamp: string;
}

export interface TrendData {
  trend: 'upward' | 'downward' | 'stable';
  volume: number;
  category: string;
  timestamp: string;
}

export interface ApiConfig {
  apiKey: string;
  baseUrl: string;
  timeout?: number;
  retries?: number;
}