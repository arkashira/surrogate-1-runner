/**
 * Dashboard client‑side logic.
 *
 * Fetches real‑time cost optimization recommendations from the backend
 * and renders them into the dashboard.
 *
 * Expected API response (JSON):
 * [
 *   {
 *     "id": "rec-123",
 *     "description": "Terminate idle EC2 instances in us-east-1",
 *     "estimatedSavings": 42.5,   // USD per month
 *     "resourceType": "EC2",
 *     "resourceId": "i-0abcd1234efgh5678"
 *   },
 *   ...
 * ]
 */

(function () {
  const API_ENDPOINT = '/api/cost-recommendations';
  const container = document.getElementById('recommendations-container');

  /**
   * Render a single recommendation.
   * @param {Object} rec
   */
  function renderRecommendation(rec) {
    const div = document.createElement('div');
    div.className = 'recommendation';
    const title = document.createElement('h4');
    title.textContent = rec.description;
    const savings = document.createElement('p');
    savings.className = 'savings';
    savings.textContent = `Estimated Savings: $${rec.estimatedSavings.toFixed(2)} / month`;
    const details = document.createElement('p');
    details.textContent = `Resource: ${rec.resourceType} (${rec.resourceId})`;
    div.appendChild(title);
    div.appendChild(savings);
    div.appendChild(details);
    return div;
  }

  /**
   * Render the full list of recommendations.
   * @param {Array} recommendations
   */
  function renderRecommendations(recommendations) {
    // Clear any existing content
    container.innerHTML = '';
    if (!recommendations.length) {
      const empty = document.createElement('p');
      empty.textContent = 'No cost optimization opportunities detected.';
      container.appendChild(empty);
      return;
    }
    recommendations.forEach(rec => {
      container.appendChild(renderRecommendation(rec));
    });
  }

  /**
   * Show an error message in the UI.
   * @param {string} msg
   */
  function renderError(msg) {
    container.innerHTML = '';
    const err = document.createElement('p');
    err.className = 'error';
    err.textContent = `Error loading recommendations: ${msg}`;
    container.appendChild(err);
  }

  /**
   * Fetch recommendations from the backend.
   */
  async function fetchRecommendations() {
    try {
      const response = await fetch(API_ENDPOINT, { credentials: 'same-origin' });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      if (!Array.isArray(data)) {
        throw new Error('Invalid response format');
      }
      renderRecommendations(data);
    } catch (err) {
      console.error('Failed to fetch cost recommendations:', err);
      renderError(err.message);
    }
  }

  // Initialise on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fetchRecommendations);
  } else {
    fetchRecommendations();
  }

  // Export for potential testing
  window.dashboard = {
    fetchRecommendations,
    renderRecommendations,
    renderError,
    renderRecommendation,
  };
})();