export enum OnboardingEventType {
  ONBOARDING_STARTED = 'onboarding_started',
  API_KEY_CONFIGURED = 'api_key_configured',
  TEMPLATE_SELECTED = 'template_selected',
  WORKFLOW_TRIGGERED = 'workflow_triggered',
  ONBOARDING_COMPLETED = 'onboarding_completed',
  WELCOME_EMAIL_SENT = 'welcome_email_sent',
}

/**
 * Map a human‑readable onboarding step to the canonical event type.
 * Extend this map when you add new steps.
 */
export const OnboardingStepMap: Record<string, OnboardingEventType> = {
  api_key_setup: OnboardingEventType.API_KEY_CONFIGURED,
  template_selection: OnboardingEventType.TEMPLATE_SELECTED,
  workflow_trigger: OnboardingEventType.WORKFLOW_TRIGGERED,
  onboarding_complete: OnboardingEventType.ONBOARDING_COMPLETED,
};