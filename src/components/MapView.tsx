import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

interface MapViewProps {
  center: [number, number];
  zoom: number;
  markers?: Array<{ position: [number, number]; popupText: string }>;
}

const MapView: React.FC<MapViewProps> = ({ center, zoom, markers }) => {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {markers?.map((marker, index) => (
        <Marker key={index} position={marker.position}>
          <Popup>{marker.popupText}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapView;