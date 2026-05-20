/**
 * Zoom SDK wrapper for injecting AudioGain Guard into the meeting audio pipeline.
 *
 * This module exposes an `initAudioGainGuard` function that:
 *   1. Dynamically injects a script tag to load the AudioGain Guard library.
 *   2. Replaces Zoom's default audio source with an AudioGainGuardSource instance.
 *
 * The AudioGainGuardSource uses the Web Audio API to apply a configurable gain
 * to the microphone stream, ensuring a stable RMS level even when Zoom's
 * internal AGC is toggled.
 */

const AudioGainGuardSource = class {
  constructor() {
    // Create an AudioContext and a GainNode for controlling volume.
    this.audioContext =
      new (window.AudioContext || window.webkitAudioContext)();
    this.gainNode = this.audioContext.createGain();
    this.gainNode.gain.value = 1.0; // Default gain
    this.sourceNode = null;
  }

  /**
   * Returns a MediaStream that is processed through the gain node.
   * @returns {Promise<MediaStream>}
   */
  async getAudioStream() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = this.audioContext.createMediaStreamSource(stream);
    source.connect(this.gainNode);
    this.gainNode.connect(this.audioContext.destination);
    this.sourceNode = source;
    return stream;
  }

  /**
   * Adjusts the gain value applied to the audio stream.
   * @param {number} value - Gain multiplier (e.g., 1.0 = no change).
   */
  setGain(value) {
    this.gainNode.gain.value = value;
  }
};

/**
 * Replaces Zoom's default audio source with an instance of AudioGainGuardSource.
 * Throws if ZoomSDK is not available on the global window object.
 */
function replaceZoomAudioSource() {
  if (!window.ZoomSDK) {
    throw new Error('ZoomSDK not found');
  }
  const guard = new AudioGainGuardSource();
  // Assume ZoomSDK exposes a method to set the audio source.
  window.ZoomSDK.setAudioSource(guard);
}

/**
 * Initializes the AudioGain Guard by loading its script and replacing the audio source.
 *
 * @param {Object} [options] - Optional configuration.
 * @param {string} [options.scriptUrl] - URL of the AudioGain Guard script.
 * @param {Function} [options.onReady] - Callback invoked after successful initialization.
 * @returns {Promise<void>}
 */
function initAudioGainGuard({ scriptUrl, onReady } = {}) {
  const defaultUrl = 'https://cdn.axentx.com/audio-gain-guard.js';
  const src = scriptUrl || defaultUrl;

  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;

    script.onload = () => {
      try {
        replaceZoomAudioSource();
        if (onReady) onReady();
        resolve();
      } catch (e) {
        reject(e);
      }
    };

    script.onerror = () =>
      reject(new Error(`Failed to load script ${src}`));

    document.head.appendChild(script);
  });
}

module.exports = {
  initAudioGainGuard,
  AudioGainGuardSource,
};