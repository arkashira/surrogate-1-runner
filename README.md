import { MapView, Overlay } from 'surrogate-1';

function App() {
  const markers = [
    { position: { lat: 51.5, lng: -0.09 }, label: "Marker 1" },
    { position: { lat: 51.51, lng: -0.1 }, label: "Marker 2" }
  ];

  return (
    <MapView
      center={{ lat: 51.505, lng: -0.09 }}
      zoom={13}
      mapProvider="google"
    >
      <Overlay markers={markers} />
    </MapView>
  );
}