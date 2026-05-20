document.addEventListener('DOMContentLoaded', () => {
  const tableBody = document.querySelector('#forecastTable tbody');
  const accuracyEl = document.getElementById('accuracy');
  const statusEl = document.getElementById('status');
  const exportBtn = document.getElementById('exportBtn');

  // ---------- Helper: CSV export ----------
  const exportTableToCSV = (filename = 'cost_forecasts.csv') => {
    const rows = Array.from(tableBody.querySelectorAll('tr'));
    if (!rows.length) return; // nothing to export

    const csv = [
      ['Date', 'Forecasted Cost ($)', 'Confidence Interval (95%)'],
      ...rows.map(row => [
        row.cells[0].textContent,
        row.cells[1].textContent,
        row.cells[2].textContent
      ])
    ]
      .map(r => r.join(','))
      .join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // ---------- Fetch & render ----------
  const loadForecasts = async () => {
    statusEl.textContent = 'Loading forecasts…';
    try {
      const res = await fetch('/api/forecasts');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // Update accuracy
      if (typeof data.accuracy === 'number')
        accuracyEl.textContent = data.accuracy.toFixed(2);

      // Populate table
      tableBody.innerHTML = '';
      data.forecasts.forEach(f => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${f.date}</td>
          <td>${f.cost.toFixed(2)}</td>
          <td>${f.confidence_interval}</td>
        `;
        tableBody.appendChild(tr);
      });

      statusEl.textContent = 'Forecasts loaded.';
    } catch (err) {
      console.error('Failed to load forecasts:', err);
      tableBody.innerHTML = '<tr><td colspan="3">Failed to load data.</td></tr>';
      statusEl.textContent = 'Error loading forecasts.';
    }
  };

  // ---------- Event listeners ----------
  exportBtn.addEventListener('click', exportTableToCSV);
  loadForecasts();
});