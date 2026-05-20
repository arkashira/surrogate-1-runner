/**
 * Dashboard module for displaying cost insights and recommendations.
 *
 * This script:
 *   - Fetches mock data (replace with real API calls).
 *   - Renders a responsive table with cost insights.
 *   - Provides filtering and sorting capabilities.
 *   - Adapts layout for mobile devices using CSS media queries.
 *
 * Dependencies:
 *   - None (vanilla JS). Ensure this script is included after the DOM is ready.
 */

(function () {
  'use strict';

  // Mock data – replace with real API endpoint
  const mockData = [
    { id: 1, service: 'Compute', cost: 120.50, recommendation: 'Use spot instances' },
    { id: 2, service: 'Storage', cost: 45.00, recommendation: 'Delete unused snapshots' },
    { id: 3, service: 'Database', cost: 300.75, recommendation: 'Scale down read replicas' },
    { id: 4, service: 'Networking', cost: 60.20, recommendation: 'Optimize routing' },
    { id: 5, service: 'AI/ML', cost: 500.00, recommendation: 'Use preemptible GPUs' }
  ];

  // State
  let data = [...mockData];
  let currentSort = { column: 'service', direction: 'asc' };
  let currentFilter = '';

  // DOM elements
  const tableBody = document.querySelector('#dashboard-table tbody');
  const filterInput = document.querySelector('#dashboard-filter');
  const sortHeaders = document.querySelectorAll('#dashboard-table th[data-sort]');

  // Render table rows
  function renderRows() {
    tableBody.innerHTML = '';
    data.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${row.service}</td>
        <td>${row.cost.toFixed(2)}</td>
        <td>${row.recommendation}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  // Sort data
  function sortData(column) {
    if (currentSort.column === column) {
      currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
      currentSort.column = column;
      currentSort.direction = 'asc';
    }
    data.sort((a, b) => {
      if (a[column] < b[column]) return currentSort.direction === 'asc' ? -1 : 1;
      if (a[column] > b[column]) return currentSort.direction === 'asc' ? 1 : -1;
      return 0;
    });
    updateSortIndicators();
    renderRows();
  }

  // Update sort indicators in table headers
  function updateSortIndicators() {
    sortHeaders.forEach(th => {
      th.classList.remove('asc', 'desc');
      if (th.dataset.sort === currentSort.column) {
        th.classList.add(currentSort.direction);
      }
    });
  }

  // Filter data
  function filterData() {
    const filter = currentFilter.toLowerCase();
    data = mockData.filter(row =>
      row.service.toLowerCase().includes(filter) ||
      row.recommendation.toLowerCase().includes(filter)
    );
    sortData(currentSort.column); // Re-apply sorting after filtering
  }

  // Event listeners
  filterInput.addEventListener('input', e => {
    currentFilter = e.target.value;
    filterData();
  });

  sortHeaders.forEach(th => {
    th.addEventListener('click', () => sortData(th.dataset.sort));
  });

  // Initial render
  renderRows();
  updateSortIndicators();

  // Expose for testing
  window.dashboard = {
    data,
    sortData,
    filterData,
    mockData
  };
})();