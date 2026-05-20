export interface AnalyticsRecord {
  /** ISO date string, e.g. "2023-01-01" */
  date: string;
  /** Metric representing daily active users, sessions, etc. */
  engagement: number;
  /** % of users that completed onboarding on that day */
  onboardingCompletion: number;
}