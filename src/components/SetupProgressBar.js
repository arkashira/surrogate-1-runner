import React from 'react';
import PropTypes from 'prop-types';

const SetupProgressBar = ({ progress }) => {
  return (
    <div className="progress-bar">
      <div className="progress" style={{ width: `${progress}%` }}></div>
    </div>
  );
};

SetupProgressBar.propTypes = {
  progress: PropTypes.number.isRequired,
};

export default SetupProgressBar;