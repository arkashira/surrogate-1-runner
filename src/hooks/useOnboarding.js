import { useSelector, useDispatch } from 'react-redux';
import {
  nextStep,
  prevStep,
  skipStep,
  completeOnboarding,
  resetOnboarding,
  setPreferences,
} from '../store/onboardingSlice';
import { steps } from '../config/onboardingSteps';

export const useOnboarding = () => {
  const dispatch = useDispatch();
  const { step, isComplete, preferences } = useSelector((s) => s.onboarding);

  const currentStep = steps[step];

  return {
    step,
    isComplete,
    preferences,
    currentStep,
    nextStep: () => dispatch(nextStep()),
    prevStep: () => dispatch(prevStep()),
    skipStep: () => dispatch(skipStep()),
    completeOnboarding: () => dispatch(completeOnboarding()),
    resetOnboarding: () => dispatch(resetOnboarding()),
    setPreferences: (prefs) => dispatch(setPreferences(prefs)),
  };
};