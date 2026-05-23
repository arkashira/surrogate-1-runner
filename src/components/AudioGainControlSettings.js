import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { getGainSettings, setGainSettings } from '../services/AudioGainControlService';

/**
 * AudioGainControlSettings
 *
 * A simple UI component that allows a meeting organizer to view and adjust
 * the audio gain setting for a specific meeting. The component fetches the
 * current gain value on mount, displays a slider (0-100 dB), and persists
 * changes via the AudioGainControlService.
 *
 * Props:
 * - meetingId (string): Identifier of the meeting to configure.
 * - onChange (function, optional): Callback invoked after a successful
 *   update with the new gain value.
 */
const AudioGainControlSettings = ({ meetingId, onChange }) => {
  const [gain, setGain] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch current gain setting when component mounts or meetingId changes
  useEffect(() => {
    let isMounted = true;
    const fetchGain = async () => {
      setLoading(true);
      setError(null);
      try {
        const currentGain = await getGainSettings(meetingId);
        if (isMounted) setGain(currentGain);
      } catch (e) {
        if (isMounted) setError('Failed to load gain setting.');
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchGain();
    return () => {
      isMounted = false;
    };
  }, [meetingId]);

  const handleChange = async (e) => {
    const newGain = Number(e.target.value);
    setGain(newGain);
    try {
      await setGainSettings(meetingId, newGain);
      if (onChange) onChange(newGain);
    } catch (e) {
      setError('Failed to update gain setting.');
    }
  };

  if (loading) return <div>Loading audio gain settings...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ margin: '1rem 0' }}>
      <label htmlFor={`audio-gain-${meetingId}`} style={{ display: 'block', marginBottom: '0.5rem' }}>
        Audio Gain (dB): {gain}
      </label>
      <input
        id={`audio-gain-${meetingId}`}
        type="range"
        min="0"
        max="100"
        step="1"
        value={gain}
        onChange={handleChange}
        style={{ width: '100%' }}
      />
    </div>
  );
};

AudioGainControlSettings.propTypes = {
  meetingId: PropTypes.string.isRequired,
  onChange: PropTypes.func,
};

export default AudioGainControlSettings;