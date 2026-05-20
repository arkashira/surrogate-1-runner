import React from 'react';
import MapView from './MapView';
import Overlay from './Overlay';

const MapWithOverlay: React.FC = () => {
  const center: [number, number] = [51.505, -0.09];
  const zoom = 13;
  const markers = [
    { position: [51.505, -0.09] as [number, number], popupText: 'Marker 1' },
    { position: [51.51, -0.1] as [number, number], popupText: 'Marker 2' },
  ];

  return (
    <div style={{ position: 'relative', height: '100vh', width: '100vw' }}>
      <MapView center={center} zoom={zoom} markers={markers} />
      <Overlay position="top-right">
        <h2>Overlay Content</h2>
        <p>This is an example of an overlay on the map.</p>
      </Overlay>
    </div>
  );
};

export default MapWithOverlay;