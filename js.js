(() => {
  /**
   * Fetch alert data.
   * Replace this mock with a real API call (e.g., fetch('/api/alerts/latest')).
   */
  async function fetchAlertData() {
    // Simulate network latency
    await new Promise(r => setTimeout(r, 500));

    // Mock payload – in production, parse the real response
    return {
      timestamp: new Date().toISOString(),
      pipeline: "data-ingest-01",
      api: "/v1/ingest"
    };
  }

  /**
   * Render data into the DOM.
   */
  function renderAlert({ timestamp, pipeline, api }) {
    document.getElementById('alert-timestamp').textContent = timestamp;
    document.getElementById('alert-pipeline').textContent = pipeline;
    document.getElementById('alert-api').textContent = api;
  }

  /**
   * Initialize the alert component.
   */
  async function init() {
    try {
      const data = await fetchAlertData();
      renderAlert(data);
    } catch (err) {
      console.error('Failed to load alert data', err);
      // Fallback UI – keep the alert visible but indicate loading failure
      document.getElementById('alert-timestamp').textContent = 'Error loading alert';
    }
  }

  // Kick off when the DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();