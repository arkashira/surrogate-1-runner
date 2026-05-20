const Recording = require('../models/Recording');

class RecordingController {
  async getAllRecordings(req, res) {
    try {
      const userId = req.user.id;
      const recordings = await Recording.getAllRecordings(userId);
      res.json(recordings);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Failed to fetch recordings' });
    }
  }

  async getRecordingById(req, res) {
    try {
      const recordingId = req.params.id;
      const recording = await Recording.getRecordingById(recordingId);
      if (!recording) {
        res.status(404).json({ message: 'Recording not found' });
      } else {
        res.json(recording);
      }
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Failed to fetch recording' });
    }
  }
}

module.exports = RecordingController;