/**
 * Dashboard analytics module – pure functions + tiny I/O wrapper.
 *
 * • Reads `data/records.json` (if present) – otherwise falls back to [].
 * • Computes deterministic aggregates.
 * • Exported helpers are fully unit‑testable.
 */

const fs = require('fs');
const path = require('path');

/* --------------------------------------------------------------
   1️⃣ Load raw records from the JSON file.
   -------------------------------------------------------------- */
function loadRecords() {
  const dataPath = path.resolve(__dirname, '../../data/records.json');
  try {
    const raw = fs.readFileSync(dataPath, 'utf8');
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (_) {
    // Missing file, unreadable, or malformed → empty dataset.
    return [];
  }
}

/* --------------------------------------------------------------
   2️⃣ Compute the analytics payload.
   -------------------------------------------------------------- */
function computeAnalytics(records) {
  const totalStartups = new Set(records.map(r => r.startupId)).size;
  const totalFounders = new Set(records.map(r => r.founderId)).size;

  const feedbackRecords = records.filter(r => r.feedbackGiven);
  const feedbackCount = feedbackRecords.length;
  const avgFeedbackScore =
    feedbackCount > 0
      ? feedbackRecords.reduce((sum, r) => sum + (r.feedbackScore || 0), 0) /
        feedbackCount
      : 0;

  const progressValues = records
    .map(r => r.progress)
    .filter(v => typeof v === 'number');

  const avgProgress =
    progressValues.length > 0
      ? progressValues.reduce((s, v) => s + v, 0) / progressValues.length
      : 0;

  // Extendable – add more derived fields here.
  return {
    totalStartups,
    totalFounders,
    feedbackCount,
    avgFeedbackScore: Number(avgFeedbackScore.toFixed(2)),
    avgProgress: Number(avgProgress.toFixed(2)),
  };
}

/* --------------------------------------------------------------
   3️⃣ Exported for the router (and for tests).
   -------------------------------------------------------------- */
module.exports = {
  loadRecords,
  computeAnalytics,
};