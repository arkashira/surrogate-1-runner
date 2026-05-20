/**
 * Minimal logger that mirrors the API used in the original codebase.
 * Swap this file with a full‑featured logger (winston, pino, etc.) without
 * touching the resolver logic.
 */
const levels = ['error', 'warn', 'info', 'debug'];

function makeLogger(prefix = '') {
  const logger = {};
  for (const lvl of levels) {
    logger[lvl] = (...args) => {
      const ts = new Date().toISOString();
      console[lvl](`[${ts}]${prefix ? ` [${prefix}]` : ''}`, ...args);
    };
  }
  return logger;
}

module.exports = makeLogger('surrogate-1');