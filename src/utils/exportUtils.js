const { generatePDF, savePDF } = require('./pdfGenerator');

async function exportData(data, format, filename) {
  switch (format) {
    case 'pdf':
      const pdfBytes = await generatePDF(data);
      savePDF(pdfBytes, filename);
      break;
    case 'csv':
      // Implement CSV generation logic here
      break;
    default:
      throw new Error('Unsupported format');
  }
}

module.exports = {
  exportData,
};