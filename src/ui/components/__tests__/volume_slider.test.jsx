import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import VolumeSlider from '../volume_slider';

describe('VolumeSlider', () => {
  it('renders with initial volume', () => {
    render(<VolumeSlider initialVolume={500} />);
    expect(screen.getByText('500 records')).toBeInTheDocument();
  });

  it('updates volume when slider is moved', () => {
    const handleChange = jest.fn();
    render(<VolumeSlider initialVolume={1000} onChange={handleChange} />);
    
    const slider = screen.getByRole('slider');
    fireEvent.change(slider, { target: { value: '2500' } });
    
    expect(handleChange).toHaveBeenCalledWith(2500);
    expect(screen.getByText('2.5k records')).toBeInTheDocument();
  });

  it('displays volume in k format for large values', () => {
    render(<VolumeSlider initialVolume={8500} />);
    expect(screen.getByText('8.5k records')).toBeInTheDocument();
  });

  it('has correct min/max values', () => {
    render(<VolumeSlider />);
    const slider = screen.getByRole('slider');
    expect(slider).toHaveAttribute('min', '100');
    expect(slider).toHaveAttribute('max', '10000');
  });
});