import React from 'react';
import PropTypes from 'prop-types';
import './ValidationBadge.css';

/**
 * Simple badge that shows a green checkmark when validation passes,
 * or a red cross when there are errors.
 *
 * @param {Object} props
 * @param {boolean} props.isValid - true if there are no errors.
 */
export default function ValidationBadge({ isValid }) {
  return (
    <div className={`validation-badge ${isValid ? 'valid' : 'invalid'}`}>
      {isValid ? '✓' : '✗'}
    </div>
  );
}

ValidationBadge.propTypes = {
  isValid: PropTypes.bool.isRequired,
};