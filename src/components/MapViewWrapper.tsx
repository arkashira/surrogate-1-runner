import React, { useEffect, useRef } from 'react';
import {
  MapView,
  MapViewProps,
  Marker,
  MarkerProps,
  PROVIDER_GOOGLE,
} from 'react-native-maps';
import { ViewStyle } from 'react-native';

/**
 * MapViewWrapper
 *
 * A thin wrapper around `react-native-maps`'s `MapView` that safely handles
 * mounting and unmounting lifecycle events to avoid memory-leak crashes on
 * both Android and iOS. All props accepted by `MapView` are re-exposed so
 * the component can be used as a drop-in replacement.
 *
 * This wrapper ensures proper cleanup of native resources during component
 * unmount to prevent memory leaks and crashes.
 *
 * Usage:
 *