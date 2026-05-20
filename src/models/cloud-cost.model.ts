export interface CloudCost {
  id: string;
  provider: 'aws' | 'gcp' | 'azure';
  amount: number;
  date: string; // ISO 8601 date string
  timestamp: Date;
}