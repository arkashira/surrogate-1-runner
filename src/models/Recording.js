class Recording {
  constructor(id, title, date, duration) {
    this.id = id;
    this.title = title;
    this.date = date;
    this.duration = duration;
  }

  static async getAllRecordings(userId) {
    try {
      const response = await axios.get(`https://example.com/recordings/${userId}`);
      const recordings = response.data;
      return recordings.map((recording) => new Recording(recording.id, recording.title, recording.date, recording.duration));
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  static async getRecordingById(recordingId) {
    try {
      const response = await axios.get(`https://example.com/recordings/${recordingId}`);
      const recording = response.data;
      return new Recording(recording.id, recording.title, recording.date, recording.duration);
    } catch (error) {
      console.error(error);
      return null;
    }
  }
}

module.exports = Recording;