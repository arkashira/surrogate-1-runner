import React, {
  useRef,
  useEffect,
  useCallback,
  useState,
  PropsWithChildren,
} from 'react';
import {
  MapView,
  MapViewProps,
  Marker,
  MarkerProps,
  Polyline,
  PolylineProps,
  Polygon,
  PolygonProps,
  Circle,
  CircleProps,
  Callout,
  CalloutProps,
  PROVIDER_GOOGLE,
  PROVIDER_DEFAULT,
} from 'react-native-maps';
import {
  View,
  StyleSheet,
  ViewStyle,
  Platform,
  AppState,
  AppStateStatus,
} from 'react-native';

/**
 * Props that extend the native `MapView` API with lifecycle helpers.
 *
 * @property enableLifecycleManagement - When `true` (default) the wrapper will
 *   automatically clean up the native view reference on unmount.
 * @property onMapReady - Called when the underlying `MapView` fires its
 *   `onMapReady` event.
 * @property onMapDestroyed - Called just before the component unmounts.
 * @property containerStyle - Style applied to the wrapper’s outer `View`.
 * @property debugMode - When `true` the wrapper prefixes all console logs
 *   with `[MapViewWrapper]`. Useful during development.
 * @property children - Any `Marker`, `Polyline`, etc. that you want to render
 *   inside the map.
 */
export interface MapViewWrapperProps
  extends Omit<MapViewProps, 'provider'>,
    PropsWithChildren {
  enableLifecycleManagement?: boolean;
  onMapReady?: () => void;
  onMapDestroyed?: () => void;
  containerStyle?: ViewStyle;
  debugMode?: boolean;
}

/**
 * A lifecycle‑aware wrapper around `react-native-maps`’ `MapView`.
 *
 * The component forwards **all** `MapView` props (except `provider`) and
 * exposes a small set of helpers that make the map safe to use in a
 * React‑Native application.
 *
 * @example
 *