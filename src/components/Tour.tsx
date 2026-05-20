import React, { useState } from 'react';
import './Tour.css';

interface TourStep {
  id: number;
  title: string;
  content: string;
  target: string;
}

const Tour: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isTourActive, setIsTourActive] = useState<boolean>(true);

  const tourSteps: TourStep[] = [
    {
      id: 1,
      title: 'Welcome to the Platform',
      content: 'This tour will guide you through the key features of the platform.',
      target: '.welcome-section',
    },
    {
      id: 2,
      title: 'Dashboard Overview',
      content: 'Here you can see an overview of your activities and statistics.',
      target: '.dashboard-section',
    },
    {
      id: 3,
      title: 'Feature Highlights',
      content: 'Explore the various features and functionalities available to you.',
      target: '.features-section',
    },
    {
      id: 4,
      title: 'Settings and Preferences',
      content: 'Customize your experience by adjusting your settings and preferences.',
      target: '.settings-section',
    },
  ];

  const nextStep = () => {
    if (currentStep < tourSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setIsTourActive(false);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const skipTour = () => {
    setIsTourActive(false);
  };

  if (!isTourActive) {
    return null;
  }

  return (
    <div className="tour-container">
      <div className="tour-content">
        <h2>{tourSteps[currentStep].title}</h2>
        <p>{tourSteps[currentStep].content}</p>
        <div className="tour-navigation">
          <button onClick={prevStep} disabled={currentStep === 0}>
            Previous
          </button>
          <button onClick={nextStep}>
            {currentStep === tourSteps.length - 1 ? 'Finish' : 'Next'}
          </button>
          <button onClick={skipTour}>Skip Tour</button>
        </div>
      </div>
    </div>
  );
};

export default Tour;