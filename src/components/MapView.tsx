import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE, Region } from 'react-native-maps';
import { validateMapProps, mapPropTypes } from '../utils/validateMapProps';
import PropTypes from 'prop-types';

export interface MarkerData {
  coordinate: {
    latitude: number;
    longitude: number;
  };
  title?: string;
  description?: string;
}

export interface MapViewProps {
  initialRegion: Region;
  markers?: MarkerData[];
  onRegionChange?: (region: Region) => void;
  onMarkerPress?: (marker: MarkerData) => void;
}

const MapViewComponent: React.FC<MapViewProps> = ({
  initialRegion,
  markers = [],
  onRegionChange,
  onMarkerPress,
}) => {
  const mapRef = useRef<MapView>(null);

  // 1️⃣  Validate props on every render (dev only)
  useEffect(() => {
    validateMapProps({ initialRegion, markers, onRegionChange, onMarkerPress }, 'MapView');
  }, [initialRegion, markers, onRegionChange, onMarkerPress]);

  // 2️⃣  Animate to the initial region when it changes
  useEffect(() => {
    if (mapRef.current && initialRegion) {
      mapRef.current.animateToRegion(initialRegion, 1000);
    }
  }, [initialRegion]);

  const handleRegionChange = (region: Region) => {
    onRegionChange?.(region);
  };

  const handleMarkerPress = (marker: MarkerData) => {
    onMarkerPress?.(marker);
  };

  return (
    <View style={styles.container} testID="map-view">
      <MapView
        ref={mapRef}
        provider={PROVIDER_GOOGLE}
        style={styles.map}
        initialRegion={initialRegion}
        onRegionChangeComplete={handleRegionChange}
        testID="map"
      >
        {markers.map((marker, idx) => (
          <Marker
            key={idx}
            coordinate={marker.coordinate}
            title={marker.title}
            description={marker.description}
            onPress={() => handleMarkerPress(marker)}
          />
        ))}
      </MapView>
    </View>
  );
};

MapViewComponent.propTypes = mapPropTypes;

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
});

export default MapViewComponent;