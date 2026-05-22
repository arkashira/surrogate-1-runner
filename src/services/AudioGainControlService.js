class AudioGainControlService {
  constructor(meetingPlatformAPI) {
    this.meetingPlatformAPI = meetingPlatformAPI;
  }

  /**
   * Configure audio gain settings for a meeting
   * @param {string} meetingId - The ID of the meeting
   * @param {Object} settings - Audio gain configuration
   * @param {number} settings.inputGain - Input gain level (0-100)
   * @param {number} settings.outputGain - Output gain level (0-100)
   * @param {boolean} settings.autoGain - Whether to enable auto gain control
   * @returns {Promise<Object>} Updated meeting data with audio settings
   */
  async configureAudioGain(meetingId, settings) {
    // Validate input settings
    if (typeof settings.inputGain !== 'undefined' && 
        (settings.inputGain < 0 || settings.inputGain > 100)) {
      throw new Error('Input gain must be between 0 and 100');
    }

    if (typeof settings.outputGain !== 'undefined' && 
        (settings.outputGain < 0 || settings.outputGain > 100)) {
      throw new Error('Output gain must be between 0 and 100');
    }

    // Apply settings through meeting platform API
    const result = await this.meetingPlatformAPI.applyAudioGainSettings(
      meetingId, 
      settings
    );

    return result;
  }

  /**
   * Get current audio gain settings for a meeting
   * @param {string} meetingId - The ID of the meeting
   * @returns {Promise<Object>} Current audio gain settings
   */
  async getAudioGainSettings(meetingId) {
    const meeting = await this.meetingPlatformAPI.getMeeting(meetingId);
    return meeting.audioGainSettings || {};
  }

  /**
   * Reset audio gain settings to defaults
   * @param {string} meetingId - The ID of the meeting
   * @returns {Promise<Object>} Updated meeting data with default settings
   */
  async resetAudioGainSettings(meetingId) {
    const result = await this.meetingPlatformAPI.applyAudioGainSettings(
      meetingId, 
      {
        inputGain: 50,
        outputGain: 50,
        autoGain: true
      }
    );

    return result;
  }

  /**
   * Validate audio gain settings before applying
   * @param {Object} settings - Audio gain configuration to validate
   * @returns {Object} Validation result
   */
  validateSettings(settings) {
    const errors = [];

    if (typeof settings.inputGain !== 'undefined' && 
        (settings.inputGain < 0 || settings.inputGain > 100)) {
      errors.push('Input gain must be between 0 and 100');
    }

    if (typeof settings.outputGain !== 'undefined' && 
        (settings.outputGain < 0 || settings.outputGain > 100)) {
      errors.push('Output gain must be between 0 and 100');
    }

    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = AudioGainControlService;