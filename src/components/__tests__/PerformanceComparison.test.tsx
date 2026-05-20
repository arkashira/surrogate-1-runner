import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import PerformanceComparison from '../PerformanceComparison';
import { GamePerformanceData } from '../../types';

const mockCurrentSetup: GamePerformanceData[] = [
  { game: 'Game A', fps: 60, component: 'GPU', cost: 500 },
  { game: 'Game B', fps: 75, component: 'CPU', cost: 300 },
];

const mockProposedSetup: GamePerformanceData[] = [
  { game: 'Game A', fps: 120, component: 'GPU', cost: 500 },
  { game: 'Game B', fps: 150, component: 'CPU', cost: 300 },
];

describe('PerformanceComparison', () => {
  it('renders current setup by default', () => {
    render(<PerformanceComparison currentSetup={mockCurrentSetup} proposedSetup={mockProposedSetup} />);
    expect(screen.getByText('Game A')).toBeInTheDocument();
    expect(screen.getByText('60')).toBeInTheDocument();
  });

  it('toggles between current and proposed setup', () => {
    render(<PerformanceComparison currentSetup={mockCurrentSetup} proposedSetup={mockProposedSetup} />);
    const toggleButton = screen.getByText('Show Proposed Setup');
    fireEvent.click(toggleButton);
    expect(screen.getByText('120')).toBeInTheDocument();
  });

  it('calculates ROI correctly', () => {
    render(<PerformanceComparison currentSetup={mockCurrentSetup} proposedSetup={mockProposedSetup} />);
    expect(screen.getByText('0.30')).toBeInTheDocument();
    const toggleButton = screen.getByText('Show Proposed Setup');
    fireEvent.click(toggleButton);
    expect(screen.getByText('0.30')).toBeInTheDocument();
  });
});