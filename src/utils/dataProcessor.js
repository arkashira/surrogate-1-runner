const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const csvParse = require('csv-parse/lib/sync');

async function fetchHistoricalData(source) {
  if (source.startsWith('http://') || source.startsWith('https://')) {
    const res = await fetch(source);
    if (!res.ok) throw new Error(`Failed to fetch ${source}`);
    return await res.text();
  }
  return fs.readFileSync(path.resolve(source), 'utf8');
}

function parseCSV(csvContent) {
  const records = csvParse(csvContent, {
    columns: true,
    skip_empty_lines: true,
    trim: true,
    cast: (value, context) => {
      if (context.header === 'date') return new Date(value).toISOString().split('T')[0];
      if (context.header === 'amount') return parseFloat(value);
      return value;
    }
  });

  // Validate and sort records
  return records
    .filter(r => r.date && r.amount)
    .sort((a, b) => new Date(a.date) - new Date(b.date));
}

module.exports = { fetchHistoricalData, parseCSV };