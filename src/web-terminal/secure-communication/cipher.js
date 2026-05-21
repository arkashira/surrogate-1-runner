/**
 * AES‑256‑GCM helpers.
 *
 * The key is derived from the environment variable `WEB_TERMINAL_SECRET`.
 * In production this should be a 32‑byte random value stored securely.
 */
const crypto = require('crypto');

const ALGORITHM = 'aes-256-gcm';
const KEY = crypto
  .createHash('sha256')
  .update(process.env.WEB_TERMINAL_SECRET || 'default_secret')
  .digest(); // 32 bytes
const NONCE_LEN = 12; // 96 bits

/**
 * Encrypts a UTF‑8 string.
 * @param {string} plaintext
 * @returns {string} Base64‑encoded nonce|tag|ciphertext
 */
function encrypt(plaintext) {
  const nonce = crypto.randomBytes(NONCE_LEN);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, nonce);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([nonce, tag, encrypted]).toString('base64');
}

/**
 * Decrypts the output of `encrypt`.
 * @param {string} ciphertext Base64‑encoded nonce|tag|ciphertext
 * @returns {string} Plaintext
 */
function decrypt(ciphertext) {
  const data = Buffer.from(ciphertext, 'base64');
  const nonce = data.slice(0, NONCE_LEN);
  const tag = data.slice(NONCE_LEN, NONCE_LEN + 16);
  const enc = data.slice(NONCE_LEN + 16);
  const decipher = crypto.createDecipheriv(ALGORITHM, KEY, nonce);
  decipher.setAuthTag(tag);
  const decrypted = Buffer.concat([decipher.update(enc), decipher.final()]);
  return decrypted.toString('utf8');
}

module.exports = { encrypt, decrypt };