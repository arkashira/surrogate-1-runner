import { useSelector, useDispatch } from 'react-redux';
import { nextStep, prevStep, completeTutorial, skipTutorial, resetTutorial } from '../redux/onboardingSlice';

export const useOnboarding = () => {
  const dispatch = useDispatch();
  const { tutorialCompleted, currentStep, isSkipped } = useSelector((state) => state.onboarding);

  const handleNext = () => dispatch(nextStep());
  const handlePrev = () => dispatch(prevStep());
  const handleComplete = () => dispatch(completeTutorial());
  const handleSkip = () => dispatch(skipTutorial());
  const handleReset = () => dispatch(resetTutorial());

  return {
    tutorialCompleted,
    currentStep,
    isSkipped,
    handleNext,
    handlePrev,
    handleComplete,
    handleSkip,
    handleReset,
  };
};