const { exec } = require('child_process');

/* --------------------------------------------------------------
   Configuration – tweak here if you need different timings.
   -------------------------------------------------------------- */
const CONFIG = {
  /** How long we wait *after* the AX attempt before trying a fallback. */
  initialBackoffMs: 2000,

  /** Maximum total time allowed for the whole cascade (incl. back‑off). */
  maxWindowMs: 60 * 1000,

  /** If a native CGEvent library is available, set its require path.
      Leave `null` to skip the native path entirely. */
  nativeCGEventModule: null, // e.g. 'node-macOS-event'
};

/* --------------------------------------------------------------
   Helper: simple Promise‑based delay.
   -------------------------------------------------------------- */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/* --------------------------------------------------------------
   Helper: run an AppleScript snippet via `osascript`.
   Returns a Promise that resolves on success, rejects with the
   stderr or exec error on failure.
   -------------------------------------------------------------- */
function runAppleScript(script) {
  // Collapse new‑lines so the shell sees a single argument.
  const oneLine = script.replace(/\n/g, ' ');
  return new Promise((resolve, reject) => {
    exec(`osascript -e '${oneLine}'`, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(stderr.trim() || error.message));
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

/* --------------------------------------------------------------
   Fallback #1 – AppleScript Cmd+V.
   -------------------------------------------------------------- */
async function sendCmdVAppleScript() {
  const script = `
    tell application "System Events"
      keystroke "v" using command down
    end tell
  `;
  await runAppleScript(script);
}

/* --------------------------------------------------------------
   Optional Fallback #2 – native CGEvent (if a binding is present).
   The implementation is deliberately defensive: if the module
   cannot be required or the call fails we simply return `false`
   so the resolver can continue with the AppleScript path.
   -------------------------------------------------------------- */
let nativeCreateEvent = null;
if (CONFIG.nativeCGEventModule) {
  try {
    // The external module must export a `createCGEvent` function.
    // Example: const { createCGEvent } = require('node-macOS-event');
    nativeCreateEvent = require(CONFIG.nativeCGEventModule).createCGEvent;
  } catch (e) {
    console.warn(
      `Native CGEvent module "${CONFIG.nativeCGEventModule}" could not be loaded:`,
      e.message
    );
  }
}

/**
 * Attempt to synthesize a Cmd+V using a native CoreGraphics event.
 * Returns `true` on success, `false` otherwise.
 */
async function sendCmdVCGEvent() {
  if (!nativeCreateEvent) {
    return false;
  }

  try {
    // The native helper is expected to accept a string like 'cmd+v'
    // and return an object with a `.post()` method.
    const event = nativeCreateEvent('cmd+v');
    if (!event || typeof event.post !== 'function') {
      throw new Error('Invalid event object returned by native module');
    }
    await event.post(); // may be sync or async – we await just in case
    return true;
  } catch (e) {
    console.error('Native CGEvent Cmd+V failed:', e);
    return false;
  }
}

/* --------------------------------------------------------------
   Export everything that the resolver needs.
   -------------------------------------------------------------- */
module.exports = {
  CONFIG,
  delay,
  sendCmdVAppleScript,
  sendCmdVCGEvent,
  // expose for testing / advanced usage
  runAppleScript,
};