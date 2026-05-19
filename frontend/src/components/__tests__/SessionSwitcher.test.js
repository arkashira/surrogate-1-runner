import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SessionSwitcher from '../SessionSwitcher';

describe('SessionSwitcher', () => {
  const sessions = [
    { id: '1', name: 'Session 1' },
    { id: '2', name: 'Session 2' },
  ];
  const currentSession = { id: '1', name: 'Session 1' };
  const mockSwitchSession = jest.fn();

  it('renders the current session', () => {
    render(<SessionSwitcher sessions={sessions} currentSession={currentSession} switchSession={mockSwitchSession} />);
    expect(screen.getByText('Session 1')).toBeInTheDocument();
  });

  it('highlights the current session', () => {
    render(<SessionSwitcher sessions={sessions} currentSession={currentSession} switchSession={mockSwitchSession} />);
    expect(screen.getByText('Session 1').closest('li')).toHaveClass('active');
  });

  it('switches sessions when clicked', () => {
    render(<SessionSwitcher sessions={sessions} currentSession={currentSession} switchSession={mockSwitchSession} />);
    fireEvent.click(screen.getByText('Session 2'));
    expect(mockSwitchSession).toHaveBeenCalledWith({ id: '2', name: 'Session 2' });
  });
});