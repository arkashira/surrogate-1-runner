const { createWriteStream } = require('fs');
const { PDFDocument } = require('pdf-lib');
const path = require('path');

async function generatePDF(data) {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([600, 400]);
  const { width, height } = page.getSize();

  const fontSize = 12;
  let y = height - 50;

  page.drawText('Advisor-Ready Documentation for Tax Filing', {
    x: 50,
    y,
    size: fontSize * 2,
    bold: true,
  });

  y -= fontSize * 3;

  page.drawText('Summary:', {
    x: 50,
    y,
    size: fontSize,
    bold: true,
  });

  y -= fontSize;

  if (data.summary) {
    data.summary.forEach((line) => {
      page.drawText(line, {
        x: 50,
        y,
        size: fontSize,
      });
      y -= fontSize;
    });
  }

  y -= fontSize;

  page.drawText('Calculations:', {
    x: 50,
    y,
    size: fontSize,
    bold: true,
  });

  y -= fontSize;

  if (data.calculations) {
    data.calculations.forEach((line) => {
      page.drawText(line, {
        x: 50,
        y,
        size: fontSize,
      });
      y -= fontSize;
    });
  }

  y -= fontSize;

  page.drawText('IRS Reference Links:', {
    x: 50,
    y,
    size: fontSize,
    bold: true,
  });

  y -= fontSize;

  if (data.links) {
    data.links.forEach((link) => {
      page.drawText(link, {
        x: 50,
        y,
        size: fontSize,
      });
      y -= fontSize;
    });
  }

  const pdfBytes = await pdfDoc.save();
  return pdfBytes;
}

function savePDF(pdfBytes, filename) {
  const writeStream = createWriteStream(path.join(__dirname, '..', 'exports', `${filename}.pdf`));
  writeStream.write(pdfBytes);
  writeStream.end();
}

module.exports = {
  generatePDF,
  savePDF,
};