/**
 * AudioGainControlService
 *
 * Provides helper functions to interact with the backend API for
 * retrieving and updating audio gain settings for a meeting.
 *
 * Assumptions:
 * - The backend exposes the following endpoints:
 *   GET   /api/meetings/:meetingId/audio-gain
 *   POST  /api/meetings/:meetingId/audio-gain
 *   The POST body should be JSON: { gain: number }
 * - All responses are JSON with a `gain` field.
 */

const API_BASE = '/api/meetings';

/**
 * Fetch the current audio gain setting for a meeting.
 *
 * @param {string} meetingId
 * @returns {Promise<number>} The current gain value.
 */
export const getGainSettings = async (meetingId) => {
  const response = await fetch(`${API_BASE}/${meetingId}/audio-gain`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch gain setting: ${response.status}`);
  }
  const data = await response.json();
  if (typeof data.gain !== 'number') {
    throw new Error('Invalid gain data received');
  }
  return data.gain;
};

/**
 * Update the audio gain setting for a meeting.
 *
 * @param {string} meetingId
 * @param {number} gain
 * @returns {Promise<void>}
 */
export const setGainSettings = async (meetingId, gain) => {
  const response = await fetch(`${API_BASE}/${meetingId}/audio-gain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ gain }),
  });
  if (!response.ok) {
    throw new Error(`Failed to set gain setting: ${response.status}`);
  }
  // Optionally, we could return the updated value:
  // const data = await response.json();
  // return data.gain;
};