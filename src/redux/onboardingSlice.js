import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  tutorialCompleted: false,
  currentStep: 0,
  isSkipped: false,
};

const onboardingSlice = createSlice({
  name: 'onboarding',
  initialState,
  reducers: {
    nextStep: (state) => {
      state.currentStep += 1;
    },
    prevStep: (state) => {
      state.currentStep -= 1;
    },
    completeTutorial: (state) => {
      state.tutorialCompleted = true;
    },
    skipTutorial: (state) => {
      state.isSkipped = true;
    },
    resetTutorial: (state) => {
      state.tutorialCompleted = false;
      state.currentStep = 0;
      state.isSkipped = false;
    },
  },
});

export const { nextStep, prevStep, completeTutorial, skipTutorial, resetTutorial } = onboardingSlice.actions;
export default onboardingSlice.reducer;