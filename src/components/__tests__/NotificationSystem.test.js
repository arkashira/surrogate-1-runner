import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import NotificationSystem from '../NotificationSystem';

test('renders notifications and allows dismissal without affecting other UI', () => {
  const notifications = [
    { id: '1', title: 'Gain Too Low', body: 'Please increase microphone gain.' },
    { id: '2', title: 'Gain Too High', body: 'Please decrease microphone gain.' },
  ];

  render(<NotificationSystem initialNotifications={notifications} />);

  // Verify both notifications are present
  expect(screen.getByText('Gain Too Low')).toBeInTheDocument();
  expect(screen.getByText('Gain Too High')).toBeInTheDocument();

  // Dismiss the first notification
  const dismissButtons = screen.getAllByRole('button', { name: /dismiss/i });
  fireEvent.click(dismissButtons[0]);

  // First notification should be gone, second should remain
  expect(screen.queryByText('Gain Too Low')).not.toBeInTheDocument();
  expect(screen.getByText('Gain Too High')).toBeInTheDocument();
});