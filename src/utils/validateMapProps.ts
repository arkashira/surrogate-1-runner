import PropTypes from 'prop-types';

export const mapPropTypes = {
  initialRegion: PropTypes.shape({
    latitude: PropTypes.number.isRequired,
    longitude: PropTypes.number.isRequired,
    latitudeDelta: PropTypes.number.isRequired,
    longitudeDelta: PropTypes.number.isRequired,
  }).isRequired,
  markers: PropTypes.arrayOf(
    PropTypes.shape({
      coordinate: PropTypes.shape({
        latitude: PropTypes.number.isRequired,
        longitude: PropTypes.number.isRequired,
      }).isRequired,
      title: PropTypes.string,
      description: PropTypes.string,
    })
  ),
  onRegionChange: PropTypes.func,
  onMarkerPress: PropTypes.func,
};

export function validateMapProps(props: any, componentName = 'MapView') {
  const errors: string[] = [];

  PropTypes.checkPropTypes(mapPropTypes, props, 'prop', componentName);

  // PropTypes will throw in prod, but we want a clear error message in dev.
  // If you prefer silent logging, replace the throw with console.error.
  if (process.env.NODE_ENV !== 'production' && errors.length) {
    errors.forEach(err => console.error(err));
  }
}