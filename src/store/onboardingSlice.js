import { createSlice } from '@reduxjs/toolkit';
import { steps } from '../config/onboardingSteps'; // see below

const initialState = {
  step: 0,
  isComplete: false,
  preferences: {},          // will hold user‑defined learning prefs
};

const onboardingSlice = createSlice({
  name: 'onboarding',
  initialState,
  reducers: {
    nextStep(state) {
      if (state.step < steps.length - 1) {
        state.step += 1;
      } else {
        state.isComplete = true;
      }
    },
    prevStep(state) {
      if (state.step > 0) state.step -= 1;
    },
    skipStep(state) {
      if (state.step < steps.length - 1) state.step += 1;
    },
    completeOnboarding(state) {
      state.isComplete = true;
    },
    resetOnboarding(state) {
      state.step = 0;
      state.isComplete = false;
      state.preferences = {};
    },
    setPreferences(state, action) {
      state.preferences = action.payload;
    },
  },
});

export const {
  nextStep,
  prevStep,
  skipStep,
  completeOnboarding,
  resetOnboarding,
  setPreferences,
} = onboardingSlice.actions;

export default onboardingSlice.reducer;