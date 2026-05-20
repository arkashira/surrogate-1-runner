const fs = require('fs');
const path = require('path');
const { saasConfig } = require('../config/saas_config');

class StorageManager {
  constructor() {
    this.storagePath = path.resolve(__dirname, '../data/saas_data');
    this.ensureStorageDirectory();
  }

  ensureStorageDirectory() {
    if (!fs.existsSync(this.storagePath)) {
      fs.mkdirSync(this.storagePath, { recursive: true });
    }
  }

  /**
   * Write data atomically – first to a temp file, then rename.
   * @param {string} userId
   * @param {string} type
   * @param {string} data – already encrypted JSON string
   */
  async storeData(userId, type, data) {
    const filePath = path.join(this.storagePath, `${userId}_${type}.json`);
    const tmpPath = `${filePath}.tmp`;
    await fs.promises.writeFile(tmpPath, data, 'utf8');
    await fs.promises.rename(tmpPath, filePath);
  }

  async retrieveData(userId, type) {
    const filePath = path.join(this.storagePath, `${userId}_${type}.json`);
    try {
      return await fs.promises.readFile(filePath, 'utf8');
    } catch (err) {
      if (err.code === 'ENOENT') return null;
      throw err;
    }
  }
}

module.exports = new StorageManager();