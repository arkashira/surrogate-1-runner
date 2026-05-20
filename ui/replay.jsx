import React, { useRef, useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Replay component renders a video element that plays back a terminal session recording.
 * It provides a speed control that allows the user to adjust playback speed up to 10x.
 *
 * @param {Object} props
 * @param {string} props.recordingUrl - URL of the recording (video/audio file)
 * @param {number} [props.initialSpeed=1] - Initial playback speed
 */
const Replay = ({ recordingUrl, initialSpeed = 1 }) => {
  const videoRef = useRef(null);
  const [speed, setSpeed] = useState(initialSpeed);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = speed;
    }
  }, [speed]);

  const handleSpeedChange = (e) => {
    const newSpeed = parseFloat(e.target.value);
    setSpeed(newSpeed);
  };

  return (
    <div style={styles.container}>
      <video
        ref={videoRef}
        src={recordingUrl}
        controls
        style={styles.video}
        onError={(e) => console.error('Video playback error:', e)}
      />
      <div style={styles.controls}>
        <label htmlFor="speed" style={styles.label}>
          Speed: {speed}x
        </label>
        <input
          id="speed"
          type="range"
          min="0.5"
          max="10"
          step="0.5"
          value={speed}
          onChange={handleSpeedChange}
          style={styles.slider}
        />
      </div>
    </div>
  );
};

Replay.propTypes = {
  recordingUrl: PropTypes.string.isRequired,
  initialSpeed: PropTypes.number,
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '100%',
  },
  video: {
    width: '100%',
    maxWidth: '800px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  controls: {
    marginTop: '10px',
    display: 'flex',
    alignItems: 'center',
  },
  label: {
    marginRight: '8px',
    fontSize: '14px',
  },
  slider: {
    flexGrow: 1,
  },
};

export default Replay;