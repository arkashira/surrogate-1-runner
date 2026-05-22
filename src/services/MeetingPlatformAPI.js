class MeetingPlatformAPI {
  constructor() {
    this.baseURL = process.env.MEETING_PLATFORM_API_URL || 'https://api.meetingplatform.com';
    this.apiKey = process.env.MEETING_PLATFORM_API_KEY;
  }

  async createMeeting(meetingData) {
    const response = await fetch(`${this.baseURL}/meetings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        ...meetingData,
        audioGainSettings: meetingData.audioGainSettings || {}
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to create meeting: ${response.statusText}`);
    }

    return await response.json();
  }

  async updateMeeting(meetingId, meetingData) {
    const response = await fetch(`${this.baseURL}/meetings/${meetingId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        ...meetingData,
        audioGainSettings: meetingData.audioGainSettings || {}
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to update meeting: ${response.statusText}`);
    }

    return await response.json();
  }

  async getMeeting(meetingId) {
    const response = await fetch(`${this.baseURL}/meetings/${meetingId}`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`
      }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch meeting: ${response.statusText}`);
    }

    return await response.json();
  }

  async applyAudioGainSettings(meetingId, audioGainSettings) {
    const meeting = await this.getMeeting(meetingId);
    
    // Merge new settings with existing ones
    const updatedSettings = {
      ...meeting.audioGainSettings,
      ...audioGainSettings
    };

    const response = await this.updateMeeting(meetingId, {
      audioGainSettings: updatedSettings
    });

    return response;
  }
}

module.exports = MeetingPlatformAPI;