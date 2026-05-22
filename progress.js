/**
 * Simple in-browser progress tracking for vocabulary quizzes.
 *
 * The module stores progress in localStorage under a key derived from the
 * quiz identifier. It exposes three functions:
 *
 *   - `getProgress(quizId)`   → { correct: number, total: number }
 *   - `recordAnswer(quizId, isCorrect)` → void
 *   - `resetProgress(quizId)` → void
 *
 * The progress object is persisted as JSON. If no data exists for a given
 * quizId, defaults are returned.
 */

const STORAGE_KEY_PREFIX = 'surrogate-1-vocab-progress-';

function _storageKey(quizId) {
  return `${STORAGE_KEY_PREFIX}${quizId}`;
}

export function getProgress(quizId) {
  const raw = localStorage.getItem(_storageKey(quizId));
  if (!raw) {
    return { correct: 0, total: 0 };
  }
  try {
    const data = JSON.parse(raw);
    return {
      correct: typeof data.correct === 'number' ? data.correct : 0,
      total: typeof data.total === 'number' ? data.total : 0,
    };
  } catch {
    // corrupted data, reset
    resetProgress(quizId);
    return { correct: 0, total: 0 };
  }
}

export function recordAnswer(quizId, isCorrect) {
  const progress = getProgress(quizId);
  progress.total += 1;
  if (isCorrect) {
    progress.correct += 1;
  }
  localStorage.setItem(_storageKey(quizId), JSON.stringify(progress));
}

export function resetProgress(quizId) {
  localStorage.removeItem(_storageKey(quizId));
}