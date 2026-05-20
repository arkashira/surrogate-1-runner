import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import Tour from './Tour';

describe('Tour Component', () => {
  it('renders the tour component', () => {
    const { getByText } = render(<Tour />);
    expect(getByText('Welcome to the Platform')).toBeInTheDocument();
  });

  it('navigates to the next step', () => {
    const { getByText } = render(<Tour />);
    fireEvent.click(getByText('Next'));
    expect(getByText('Dashboard Overview')).toBeInTheDocument();
  });

  it('navigates to the previous step', () => {
    const { getByText } = render(<Tour />);
    fireEvent.click(getByText('Next'));
    fireEvent.click(getByText('Previous'));
    expect(getByText('Welcome to the Platform')).toBeInTheDocument();
  });

  it('skips the tour', () => {
    const { getByText, queryByText } = render(<Tour />);
    fireEvent.click(getByText('Skip Tour'));
    expect(queryByText('Welcome to the Platform')).not.toBeInTheDocument();
  });
});