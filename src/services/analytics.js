import { trackEvent } from './analytics-provider';

export const trackStepCompletion = async (stepId, metadata = {}) => {
  console.log(`Step completed: ${stepId}`, metadata);
  
  // Track in your analytics provider
  await trackEvent('onboarding_step_completed', {
    step_id: stepId,
    timestamp: Date.now(),
    ...metadata,
  });
  
  return { success: true, stepId };
};

export const trackOnboardingComplete = async (metadata = {}) => {
  console.log('Onboarding completed', metadata);
  
  await trackEvent('onboarding_completed', {
    completed_at: Date.now(),
    ...metadata,
  });
  
  return { success: true };
};