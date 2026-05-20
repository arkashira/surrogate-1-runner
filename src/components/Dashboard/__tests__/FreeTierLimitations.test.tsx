import React from 'react';
import { render, screen } from '@testing-library/react';
import FreeTierLimitations from '../FreeTierLimitations';

describe('FreeTierLimitations', () => {
  it('renders the free tier limitations section', () => {
    render(<FreeTierLimitations />);
    expect(screen.getByText('Free Tier Limitations')).toBeInTheDocument();
    expect(screen.getByText('Here are the limitations of our free tier:')).toBeInTheDocument();
    expect(screen.getByText('Limited to 100 API calls per day')).toBeInTheDocument();
    expect(screen.getByText('No access to premium features')).toBeInTheDocument();
    expect(screen.getByText('Basic support only')).toBeInTheDocument();
    expect(screen.getByText('No custom branding')).toBeInTheDocument();
    expect(screen.getByText('Upgrade to our paid plans for more features and higher limits.')).toBeInTheDocument();
  });
});