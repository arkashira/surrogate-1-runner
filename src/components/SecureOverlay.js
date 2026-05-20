import React, { useRef, useState } from 'react';
import MapView, { Marker, Callout, Polygon } from 'react-native-maps';
import * as Location from 'expo-location';

const SecureOverlay = () => {
  const mapRef = useRef(null);
  const [region, setRegion] = useState(null);
  const [overlayData, setOverlayData] = useState(null);

  const getLocationAsync = async () => {
    let { status } = await Location.requestPermissionsAsync();
    if (status !== 'granted') {
      console.log('Permission to access location was denied');
      return;
    }

    const location = await Location.getCurrentPositionAsync();
    setRegion({
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
      latitudeDelta: 0.0922,
      longitudeDelta: 0.0421,
    });
  };

  const handleRegionChange = (region) => {
    setRegion(region);
    // Fetch overlay data based on the new region
  };

  return (
    <MapView
      ref={mapRef}
      style={{ flex: 1 }}
      region={region}
      onRegionChange={handleRegionChange}
    >
      {overlayData && (
        <>
          <Marker
            coordinate={overlayData.coordinate}
            title={overlayData.title}
            description={overlayData.description}
          >
            <Callout onPress={() => console.log('Marker pressed')}>
              <View>
                <Text>{overlayData.calloutText}</Text>
              </View>
            </Callout>
          </Marker>
          <Polygon
            coordinates={overlayData.polygonCoordinates}
            fillColor="rgba(13, 110, 253, 0.2)"
            strokeColor="rgba(13, 110, 253, 1)"
            strokeWidth={1}
          />
        </>
      )}
    </MapView>
  );
};

export default SecureOverlay;