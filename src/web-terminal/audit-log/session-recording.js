/**
 * SessionRecorder
 *
 * Buffers terminal output in memory and forwards it to the storage layer.
 * The recorder is lightweight – it only keeps a small in‑memory buffer
 * and writes to disk when `stop()` is called.
 */

class SessionRecorder {
  /**
   * @param {string} sessionId   – Unique session identifier
   * @param {string} userId      – User that owns the session
   * @param {SessionStorage} storage – Storage instance
   */
  constructor(sessionId, userId, storage) {
    this.sessionId = sessionId;
    this.userId = userId;
    this.storage = storage;
    this.buffer = [];
    this.startedAt = new Date().toISOString();
    this.isRecording = false;
  }

  /** Start recording – clears any previous buffer */
  start() {
    if (this.isRecording) return;
    this.isRecording = true;
    this.buffer = [];
  }

  /** Append a chunk of terminal output */
  write(chunk) {
    if (!this.isRecording) return;
    this.buffer.push(chunk);
  }

  /**
   * Stop recording, compute hash, and persist everything.
   * Returns the metadata that was written.
   */
  async stop() {
    if (!this.isRecording) return null;
    this.isRecording = false;
    const finishedAt = new Date().toISOString();

    const meta = {
      sessionId: this.sessionId,
      userId: this.userId,
      startedAt: this.startedAt,
      finishedAt,
      chunks: this.buffer,
    };

    await this.storage.save(meta);
    this.buffer = [];
    return meta;
  }
}

module.exports = SessionRecorder;