import React from 'react';
import { render } from '@testing-library/react';
import MapView from '../MapView';

describe('MapView', () => {
  it('renders without crashing', () => {
    const center: [number, number] = [51.505, -0.09];
    const zoom = 13;
    render(<MapView center={center} zoom={zoom} />);
  });

  it('renders with markers', () => {
    const center: [number, number] = [51.505, -0.09];
    const zoom = 13;
    const markers = [
      { position: [51.505, -0.09] as [number, number], popupText: 'Marker 1' },
      { position: [51.51, -0.1] as [number, number], popupText: 'Marker 2' },
    ];
    render(<MapView center={center} zoom={zoom} markers={markers} />);
  });
});