const { generatePDF, savePDF } = require('../src/utils/pdfGenerator');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

describe('PDF Generator', () => {
  it('should generate a PDF with provided data', async () => {
    const testData = {
      summary: ['Summary line 1', 'Summary line 2'],
      calculations: ['Calculation line 1', 'Calculation line 2'],
      links: ['Link 1', 'Link 2'],
    };

    const pdfBytes = await generatePDF(testData);
    expect(pdfBytes).toBeDefined();

    const tempFilePath = path.join(__dirname, 'temp.pdf');
    savePDF(pdfBytes, 'temp');

    const fileExists = fs.existsSync(tempFilePath);
    expect(fileExists).toBe(true);

    fs.unlinkSync(tempFilePath);
  }, 2000); // Ensure the test completes within 2 seconds
});