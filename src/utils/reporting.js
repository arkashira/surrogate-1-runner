import jsPDF from 'jspdf';
import 'jspdf-autotable';

/**
 * Generates a report payload.
 *
 * @param {Array<Object>} data - Inventory rows
 * @param {Object} options
 * @param {'csv'|'pdf'} options.format
 * @param {boolean} options.includeHeaders
 * @returns {Promise<BlobPart>} CSV string or PDF ArrayBuffer
 */
export async function generateReport(data, { format, includeHeaders }) {
  if (format === 'csv') {
    return generateCSV(data, includeHeaders);
  }
  if (format === 'pdf') {
    return generatePDF(data, includeHeaders);
  }
  throw new Error(`Unsupported format: ${format}`);
}

function generateCSV(data, includeHeaders) {
  const headers = ['Item ID', 'Name', 'Quantity', 'Last Updated'];
  const rows = data.map(item => [
    item.id,
    item.name,
    item.quantity,
    new Date(item.lastUpdated).toISOString(),
  ]);

  let csv = '';
  if (includeHeaders) csv += headers.join(',') + '\n';
  csv += rows.map(r => r.join(',')).join('\n');
  return csv;
}

function generatePDF(data, includeHeaders) {
  const doc = new jsPDF();
  const headers = [['Item ID', 'Name', 'Quantity', 'Last Updated']];

  const rows = data.map(item => [
    item.id,
    item.name,
    item.quantity,
    new Date(item.lastUpdated).toISOString(),
  ]);

  const tableData = includeHeaders ? [headers[0], ...rows] : rows;

  doc.autoTable({
    head: includeHeaders ? [headers[0]] : [],
    body: rows,
    startY: 20,
  });

  return doc.output('arraybuffer');
}