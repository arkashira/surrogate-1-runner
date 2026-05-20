import React from 'react';
import { render } from '@testing-library/react';
import OnboardingUI from './onboarding_ui';

describe('OnboardingUI', () => {
  it('renders the onboarding UI', () => {
    const { getByText } = render(<OnboardingUI />);
    expect(getByText('Surrogate-1 Onboarding')).toBeInTheDocument();
  });
});