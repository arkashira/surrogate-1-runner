
import React, { useState } from 'react';
import { useTour, Step, Steps, ActionButton } from '@react-tour/core';
import { Container, Row, Col } from 'reactstrap';

const steps = [
  {
    id: 'welcome',
    content: 'Welcome to Axentx! Let us guide you through the setup process.',
    element: '.welcome-screen',
  },
  {
    id: 'tool-setup',
    content: 'Select the tools you want to use for content creation.',
    element: '.tool-setup-screen',
  },
  {
    id: 'settings-configuration',
    content: 'Configure your settings to personalize your experience.',
    element: '.settings-screen',
  },
  {
    id: 'completion',
    content: 'Congratulations! You have successfully set up your tools.',
    element: '.completion-screen',
  },
];

export const OnboardingTour = () => {
  const { startTour, currentStep, setCurrentStep, isOpen, close } = useTour({
    steps,
    initialStepId: 'welcome',
  });

  return (
    <Container>
      <Row>
        <Col>
          {/* Render the tour steps */}
          <Steps currentStep={currentStep} />
          <ActionButton onClick={startTour} label="Start Tour" />
        </Col>
      </Row>
    </Container>
  );
};

// src/styles/OnboardingTour.css

.welcome-screen {
  /* Styles for the welcome screen */
}

.tool-setup-screen {
  /* Styles for the tool setup screen */
}

.settings-screen {
  /* Styles for the settings screen */
}

.completion-screen {
  /* Styles for the completion screen */
}