import React from 'react';
import Joyride from 'react-joyride';

const steps = [
  {
    target: '#header',
    content: 'Welcome to AxentX!',
  },
  {
    target: '#form',
    content: 'This is where you build your validation framework.',
  },
  {
    target: '#help-center',
    content: 'Need help? Check out our Help Center!',
  },
];

const OnboardingTour = () => {
  return (
    <Joyride
      steps={steps}
      continuous
      disableScrolling
      showSkipButton
      showCloseButton
    />
  );
};

export default OnboardingTour;