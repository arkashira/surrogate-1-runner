/**
 * HMAC‑SHA256 token helpers.
 *
 * Tokens are `timestamp:signature`.  The signature is an HMAC of the
 * timestamp using the secret `WEB_TERMINAL_AUTH_SECRET`.  Tokens are
 * valid for 5 minutes.
 */
const crypto = require('crypto');

const SIGN_ALGO = 'sha256';
const VALIDITY_MS = 5 * 60 * 1000; // 5 minutes
const SECRET = process.env.WEB_TERMINAL_AUTH_SECRET || 'default_auth_secret';

function generateAuthToken() {
  const ts = Date.now().toString();
  const sig = crypto.createHmac(SIGN_ALGO, SECRET).update(ts).digest('hex');
  return `${ts}:${sig}`;
}

function verifyAuthToken(token) {
  const [tsStr, sig] = token.split(':');
  if (!tsStr || !sig) return false;

  const ts = Number(tsStr);
  if (Number.isNaN(ts)) return false;
  if (Date.now() - ts > VALIDITY_MS) return false;

  const expected = crypto
    .createHmac(SIGN_ALGO, SECRET)
    .update(tsStr)
    .digest('hex');

  // timingSafeEqual requires Buffers of equal length
  try {
    return crypto.timingSafeEqual(
      Buffer.from(sig, 'hex'),
      Buffer.from(expected, 'hex')
    );
  } catch {
    return false;
  }
}

module.exports = { generateAuthToken, verifyAuthToken };