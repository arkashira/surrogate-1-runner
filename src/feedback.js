/**
 * Stores user feedback on a specific advice item.
 * In a real system this would persist to a DB; here we keep it in memory.
 */
const feedbackStore = new Map();

/**
 * @param {Object} feedback
 * @param {string} feedback.adviceId
 * @param {number} feedback.rating 1‑5
 * @param {string} [feedback.comments]
 *
 * @returns {boolean} true if stored successfully
 */
function provideFeedback(feedback) {
  if (
    !feedback ||
    typeof feedback.adviceId !== 'string' ||
    typeof feedback.rating !== 'number' ||
    feedback.rating < 1 ||
    feedback.rating > 5
  ) {
    return false;
  }

  const entry = {
    adviceId: feedback.adviceId,
    rating: feedback.rating,
    comments: feedback.comments || '',
    timestamp: new Date().toISOString()
  };

  feedbackStore.set(feedback.adviceId, entry);
  return true;
}

/**
 * Retrieve all feedback (useful for analytics).
 */
function getAllFeedback() {
  return Array.from(feedbackStore.values());
}

module.exports = { provideFeedback, getAllFeedback };