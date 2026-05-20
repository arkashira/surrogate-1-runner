export interface OnboardingData {
  apiKey: string;
  apiSecret: string;
  selectedTemplate: string;
  workflowName: string;
}

export interface Step {
  id: string;
  title: string;
  description: string;
}

export interface Template {
  id: string;
  name: string;
  description: string;
}

export interface AnalyticsEvent {
  stepId: string;
  timestamp: number;
  metadata?: Record<string, unknown>;
}