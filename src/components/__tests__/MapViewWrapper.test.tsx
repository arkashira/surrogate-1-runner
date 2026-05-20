import React from 'react';
import { render } from '@testing-library/react-native';
import MapViewWrapper from '../MapViewWrapper';
import { Marker } from 'react-native-maps';

// Mock react-native-maps to avoid native dependencies in the test environment
jest.mock('react-native-maps', () => {
  const React = require('react');
  const MockMapView = (props: any) => <>{props.children}</>;
  const MockMarker = (props: any) => <>{props.children}</>;
  return {
    __esModule: true,
    default: MockMapView,
    MapView: MockMapView,
    Marker: MockMarker,
    PROVIDER_GOOGLE: 'google',
  };
});

describe('MapViewWrapper', () => {
  it('mounts without throwing and unmounts cleanly', () => {
    const { unmount } = render(
      <MapViewWrapper
        style={{ width: 200, height: 200 }}
        initialRegion={{
          latitude: 0,
          longitude: 0,
          latitudeDelta: 0.1,
          longitudeDelta: 0.1,
        }}
      >
        <Marker coordinate={{ latitude: 0, longitude: 0 }} />
      </MapViewWrapper>
    );

    // If render succeeds, the component mounted correctly.
    // No explicit assertions needed – the test will fail on exceptions.
    unmount(); // Ensure cleanup runs without errors.
  });
});