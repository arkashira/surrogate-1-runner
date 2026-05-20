/**
 * API client for surrogate-1 web application.
 *
 * Provides functions to interact with the backend ROI calculation
 * and decision recording endpoints.
 */

export async function getRoi(payload) {
  /**
   * Send user hardware and budget data to the ROI endpoint.
   *
   * @param {Object} payload - { cpu, gpu, ram, budget }
   * @returns {Promise<Object>} - Response JSON containing recommendations.
   */
  const response = await fetch('/api/v1/roi', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`ROI request failed: ${err}`);
  }

  return response.json();
}

export async function recordDecision(payload) {
  /**
   * Record a user's decision to select a recommendation.
   *
   * @param {Object} payload - { recommendation_id, user_id }
   * @returns {Promise<Object>} - Response JSON confirming the record.
   */
  const response = await fetch('/api/v1/decision', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Decision record failed: ${err}`);
  }

  return response.json();
}