import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import OnboardingFlow from '../components/OnboardingFlow';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders OnboardingFlow component', () => {
  render(
    <Router>
      <OnboardingFlow />
    </Router>
  );
  expect(screen.getByText('Set Your Learning Goal')).toBeInTheDocument();
});

test('proceeds to feedback step after setting learning goal', () => {
  render(
    <Router>
      <OnboardingFlow />
    </Router>
  );
  fireEvent.change(screen.getByPlaceholderText('What do you want to learn?'), {
    target: { value: 'Learn React' },
  });
  fireEvent.click(screen.getByText('Next'));
  expect(screen.getByText('Feedback')).toBeInTheDocument();
});