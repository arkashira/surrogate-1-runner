export type TimeRange = 'lastHour' | 'lastDay';

export interface ResourceBreakdown {
  resourceType: string;
  cost: number;
  percentage: number;
  resourceId: string;
}