const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class LocalStorage {
  constructor() {
    this.storagePath = path.join(__dirname, '..', 'data', 'user-data.json');
    this.encryptionKey = crypto.randomBytes(32);
  }

  async init() {
    try {
      await fs.promises.access(this.storagePath);
    } catch (err) {
      await fs.promises.mkdir(path.dirname(this.storagePath), { recursive: true });
      await fs.promises.writeFile(this.storagePath, JSON.stringify({}));
    }
  }

  async getData() {
    const data = await fs.promises.readFile(this.storagePath, 'utf8');
    const decryptedData = this.decrypt(data);
    return JSON.parse(decryptedData);
  }

  async saveData(data) {
    const encryptedData = this.encrypt(JSON.stringify(data));
    await fs.promises.writeFile(this.storagePath, encryptedData);
  }

  async exportData() {
    const data = await this.getData();
    return JSON.stringify(data, null, 2);
  }

  encrypt(data) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', this.encryptionKey, iv);
    const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
    return iv.toString('hex') + ':' + encrypted.toString('hex');
  }

  decrypt(data) {
    const parts = data.split(':');
    const iv = Buffer.from(parts.shift(), 'hex');
    const encrypted = Buffer.from(parts.join(':'), 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', this.encryptionKey, iv);
    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return decrypted.toString();
  }
}

module.exports = LocalStorage;