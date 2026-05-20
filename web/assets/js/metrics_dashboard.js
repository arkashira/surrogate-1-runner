
// Initialize KPI section
const kpiSection = document.getElementById('kpi-section');
// Initialize KPI container
const kpiContainer = document.getElementById('kpi-container');

// Fetch KPIs and render them in the KPI container
async function fetchKPIs() {
  const response = await fetch('/api/metrics/kpis');
  const data = await response.json();
  data.forEach(kpi => {
    const kpiElement = document.createElement('div');
    kpiElement.textContent = kpi.name + ': ' + kpi.value;
    kpiContainer.appendChild(kpiElement);
  });
}

// Call fetchKPIs function to initialize KPIs
fetchKPIs();

// Initialize historical data section
const historicalDataSection = document.getElementById('historical-data-section');
// Initialize historical data table
const historicalDataTable = document.getElementById('historical-data-table');

// Fetch historical data and render it in the historical data table
async function fetchHistoricalData() {
  const response = await fetch('/api/metrics/historical');
  const data = await response.json();

  // Create table header row
  const headerRow = document.createElement('tr');
  data[0].forEach(header => {
    const th = document.createElement('th');
    th.textContent = header;
    headerRow.appendChild(th);
  });
  historicalDataTable.appendChild(headerRow);

  // Create table body rows
  data.slice(1).forEach(row => {
    const rowElement = document.createElement('tr');
    row.forEach(cell => {
      const td = document.createElement('td');
      td.textContent = cell;
      rowElement.appendChild(td);
    });
    historicalDataTable.appendChild(rowElement);
  });
}

// Call fetchHistoricalData function to initialize historical data
fetchHistoricalData();