/**
 * Convert an array of objects to a CSV Blob and trigger a download.
 *
 * @param {Object[]} rows          Data rows – each row is a plain object.
 * @param {string}   filename      Name of the file the browser will save.
 */
export function exportToCsv(rows, filename = 'report.csv') {
  if (!rows?.length) {
    console.warn('CSV export called with empty data');
    return;
  }

  const headers = Object.keys(rows[0]);
  const csv = [
    headers.map(h => `"${h}"`).join(','),               // header line
    ...rows.map(row =>
      headers
        .map(h => {
          const cell = row[h];
          // Escape quotes & commas
          const escaped = typeof cell === 'string'
            ? cell.replace(/"/g, '""')
            : cell;
          return `"${escaped}"`;
        })
        .join(',')
    ),
  ].join('\n');

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.setAttribute('download', filename);
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}