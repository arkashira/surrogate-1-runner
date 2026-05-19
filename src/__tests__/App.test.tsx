import React from 'react';
import { render } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
  });

  it('renders the Dashboard component', () => {
    const { getByText } = render(<App />);
    expect(getByText('CFD Simulation Troubleshooting Guide')).toBeInTheDocument();
  });
});