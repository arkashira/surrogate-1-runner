import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Replay from '../replay.jsx';

describe('Replay component', () => {
  const mockUrl = 'http://localhost/mock-recording.mp4';

  test('renders video element with correct src', () => {
    render(<Replay recordingUrl={mockUrl} />);
    const video = screen.getByRole('video');
    expect(video).toBeInTheDocument();
    expect(video).toHaveAttribute('src', mockUrl);
  });

  test('speed control updates playback rate', () => {
    render(<Replay recordingUrl={mockUrl} />);
    const slider = screen.getByLabelText(/Speed/i);
    // Set to 5x
    fireEvent.change(slider, { target: { value: '5' } });
    const video = screen.getByRole('video');
    expect(video.playbackRate).toBe(5);
  });
});