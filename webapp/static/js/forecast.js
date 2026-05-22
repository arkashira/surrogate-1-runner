/**
 * Forecast Chart Component
 *
 * This module fetches forecast data from `/forecast.json`, renders a line chart
 * with a ±10% confidence interval, and provides a CSV export button.
 *
 * Expected JSON format:
 * [
 *   { "date": "2026-05-01", "forecast": 1200, "lower": 1080, "upper": 1320 },
 *   ...
 * ]
 *
 * The chart uses Chart.js (loaded via CDN in the template).
 */

const ForecastChart = (() => {
  const API_ENDPOINT = '/forecast.json';
  const CONFIDENCE_INTERVAL = 0.10; // ±10%

  /**
   * Fetch forecast data from the API.
   * @returns {Promise<Array<{date:string, forecast:number, lower:number, upper:number}>>}
   */
  async function fetchForecast() {
    const response = await fetch(API_ENDPOINT);
    if (!response.ok) {
      throw new Error(`Failed to load forecast data: ${response.statusText}`);
    }
    const data = await response.json();
    // Ensure data is sorted by date
    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  }

  /**
   * Create a CSV string from forecast data.
   * @param {Array} data
   * @returns {string}
   */
  function toCSV(data) {
    const header = ['Date', 'Forecast', 'Lower Bound', 'Upper Bound'];
    const rows = data.map(d => [
      d.date,
      d.forecast.toFixed(2),
      d.lower.toFixed(2),
      d.upper.toFixed(2),
    ]);
    return [header, ...rows].map(r => r.join(',')).join('\n');
  }

  /**
   * Trigger a download of the CSV file.
   * @param {string} csv
   * @param {string} filename
   */
  function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  /**
   * Render the forecast chart using Chart.js.
   * @param {Array} data
   */
  function renderChart(data) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    const labels = data.map(d => d.date);
    const forecastValues = data.map(d => d.forecast);
    const lowerValues = data.map(d => d.lower);
    const upperValues = data.map(d => d.upper);

    // Destroy existing chart if any
    if (window.forecastChartInstance) {
      window.forecastChartInstance.destroy();
    }

    window.forecastChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: '30‑Day Forecast',
            data: forecastValues,
            borderColor: '#007bff',
            backgroundColor: 'rgba(0,123,255,0.1)',
            fill: false,
            tension: 0.1,
          },
          {
            label: '90‑Day Forecast',
            data: forecastValues,
            borderColor: '#28a745',
            backgroundColor: 'rgba(40,167,69,0.1)',
            fill: false,
            tension: 0.1,
            borderDash: [5, 5],
          },
          {
            label: 'Confidence Interval',
            data: lowerValues,
            borderColor: 'rgba(255,0,0,0.2)',
            backgroundColor: 'rgba(255,0,0,0.1)',
            fill: '+1', // fill between lower and upper
            tension: 0.1,
          },
          {
            label: '',
            data: upperValues,
            borderColor: 'rgba(255,0,0,0.2)',
            backgroundColor: 'rgba(255,0,0,0.1)',
            fill: false,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Cloud Spending Forecast',
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
          legend: {
            position: 'bottom',
          },
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false,
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date',
            },
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Projected Spend ($)',
            },
            beginAtZero: false,
          },
        },
      },
    });
  }

  /**
   * Initialize the forecast component.
   */
  async function init() {
    try {
      const data = await fetchForecast();
      renderChart(data);

      // Attach CSV export handler
      const exportBtn = document.getElementById('exportCsvBtn');
      if (exportBtn) {
        exportBtn.addEventListener('click', () => {
          const csv = toCSV(data);
          downloadCSV(csv, 'forecast.csv');
        });
      }
    } catch (err) {
      console.error(err);
      const container = document.getElementById('forecastContainer');
      if (container) {
        container.innerHTML = `<p class="text-danger">Error loading forecast data.</p>`;
      }
    }
  }

  // Expose public API
  return {
    init,
  };
})();

// Auto‑initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  ForecastChart.init();
});