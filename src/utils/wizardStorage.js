const STORAGE_KEY = 'onboarding_wizard_state';

const defaultState = {
  currentStep: 0,
  completedSteps: [],
  stepData: {}
};

export const saveWizardState = (state) => {
  try {
    const mergedState = { ...defaultState, ...state };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(mergedState));
  } catch (error) {
    console.warn('Failed to persist wizard state:', error);
  }
};

export const loadWizardState = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : defaultState;
  } catch (error) {
    console.warn('Failed to load wizard state:', error);
    return defaultState;
  }
};

export const clearWizardState = () => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.warn('Failed to clear wizard state:', error);
  }
};

export const isStepCompleted = (stepId, completedSteps) => 
  completedSteps.includes(stepId);