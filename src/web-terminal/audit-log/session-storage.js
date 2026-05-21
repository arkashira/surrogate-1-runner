/**
 * SessionStorage
 *
 * Persists a session to the file‑system as a gzipped JSON blob.
 * The blob contains:
 *   - sessionId, userId, timestamps
 *   - raw terminal output chunks
 *   - SHA‑256 hash of the concatenated output (for tamper detection)
 *
 * The base directory is configurable – useful for CI, dev, prod, or
 * for swapping to an object store in the future.
 */

const fs = require('fs').promises;
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const util = require('util');
const gzip = util.promisify(zlib.gzip);
const gunzip = util.promisify(zlib.gunzip);

class SessionStorage {
  /**
   * @param {string} baseDir – Root folder for all audit logs
   */
  constructor(baseDir) {
    this.baseDir = baseDir;
  }

  /** Ensure a directory exists */
  async _ensureDir(dir) {
    await fs.mkdir(dir, { recursive: true });
  }

  /**
   * Save a session.
   * @param {Object} meta – See SessionRecorder.stop()
   */
  async save(meta) {
    const { sessionId, chunks } = meta;
    const dir = path.join(this.baseDir, sessionId);
    await this._ensureDir(dir);

    // Compute hash of the raw output
    const raw = chunks.join('');
    const hash = crypto.createHash('sha256').update(raw).digest('hex');

    const payload = {
      ...meta,
      hash,
    };

    const json = JSON.stringify(payload);
    const compressed = await gzip(json);
    await fs.writeFile(path.join(dir, 'recording.json.gz'), compressed);
  }

  /**
   * Load a session – verifies the hash and returns the metadata.
   * @param {string} sessionId
   * @returns {Object}
   */
  async load(sessionId) {
    const file = path.join(this.baseDir, sessionId, 'recording.json.gz');
    const compressed = await fs.readFile(file);
    const json = await gunzip(compressed);
    const payload = JSON.parse(json.toString());

    // Verify integrity
    const raw = payload.chunks.join('');
    const expected = crypto.createHash('sha256').update(raw).digest('hex');
    if (expected !== payload.hash) {
      throw new Error(`Integrity check failed for session ${sessionId}`);
    }
    return payload;
  }
}

module.exports = SessionStorage;