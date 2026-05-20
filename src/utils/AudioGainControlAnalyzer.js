/**
 * Analyze the current audio gain value and determine if it is within an
 * optimal range for transcription accuracy.
 *
 * @param {number} gainValue - Normalized gain value (0.0 – 1.0).
 * @returns {{optimized: boolean, message: string}} Result object.
 *
 * The optimal range is defined as 0.20 – 0.80. Values outside this range are
 * considered non‑optimal and a user‑friendly instruction is returned.
 */
export function analyzeAudioGain(gainValue) {
  const THRESH_LOW = 0.2;
  const THRESH_HIGH = 0.8;

  const optimized = gainValue >= THRESH_LOW && gainValue <= THRESH_HIGH;

  let message;
  if (optimized) {
    message = 'Audio gain is within the optimal range.';
  } else if (gainValue < THRESH_LOW) {
    message = `Audio gain (${gainValue.toFixed(2)}) is too low. Increase your microphone gain to improve transcription accuracy.`;
  } else {
    message = `Audio gain (${gainValue.toFixed(2)}) is too high. Decrease your microphone gain to avoid clipping and improve transcription accuracy.`;
  }

  return { optimized, message };
}